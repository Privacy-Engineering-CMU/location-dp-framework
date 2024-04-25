from dataset import *
from preprocessor import *
from localDP import *
from tqdm import tqdm
import pickle
import pandas as pd
import os
from copy import deepcopy
from streamlit_folium import folium_static
import folium
import streamlit as st

@st.cache(hash_funcs={folium.folium.Map: lambda _: None}, allow_output_mutation=True)
def make_map(df, diff_steps, display_all=True):
	if display_all:
		main_map = folium.Map(location=(40.4432, -79.9428), zoom_start=14)
		for row in df:
			# Calculate bounds for the rectangle
			bottom_left = [float(row[-3]) - diff_steps[0]/2, float(row[-2]) - diff_steps[1]/2]
			top_right = [float(row[-3]) + diff_steps[0]/2, float(row[-2]) + diff_steps[1]/2]
			bounds = [bottom_left, top_right]
			
			# Define rectangle in GeoJSON format
			if not np.issubdtype(type(row[-1]), np.str_):
				feature = {
					"type": "Feature",
					"properties": {
						"tooltip": f"{round(row[-1], 3)}"
					},
					"geometry": {
						"type": "Polygon",
						"coordinates": [[[b[1], b[0]] for b in [bottom_left, [bottom_left[0], top_right[1]], top_right, [top_right[0], bottom_left[1]], bottom_left]]]
					}
				}
			else:
				tooltip_text = str(row[-1]).replace("\n", "<br>")
				feature = {
					"type": "Feature",
					"properties": {
						"tooltip": tooltip_text
					},
					"geometry": {
						"type": "Polygon",
						"coordinates": [[[b[1], b[0]] for b in [bottom_left, [bottom_left[0], top_right[1]], top_right, [top_right[0], bottom_left[1]], bottom_left]]]
					}
				}
			
			# Create a GeoJson object and add it to the map
			geo_json = folium.GeoJson(
				feature,
				style_function=lambda x: {
					'fillColor': 'blue',
					'color': 'white',
					'fillOpacity': 0.2,
					'weight': 1
				},
				highlight_function=lambda x: {
					'fillColor': 'orange',  # Color on hover
					'color': 'white',
					'fillOpacity': 0.4,
					'weight': 1
				},
				tooltip=folium.features.GeoJsonTooltip(
					fields=['tooltip'],
					aliases=['Value:'],
					localize=True
				)
			).add_to(main_map)
	return main_map

def communicate(a, b, output_dir, user_id):
	os.makedirs(output_dir, exist_ok=True)
	file_path_a = os.path.join(output_dir, f"user_{user_id}_a.pkl")
	file_path_b = os.path.join(output_dir, f"user_{user_id}_b.pkl")
	with open(file_path_a, 'wb') as file_a:
		pickle.dump(a, file_a)
	with open(file_path_b, 'wb') as file_b:
		pickle.dump(b, file_b)

def aggregate_from_output_dir(output_dir, datatype):
	data_a = []
	data_b = []
	files = os.listdir(output_dir)
	for file in files:
		if file.endswith("_a.pkl"):
			full_path = os.path.join(output_dir, file)
			with open(full_path, 'rb') as f:
				data = pickle.load(f)
				data_a.append(data)
		elif file.endswith("_b.pkl"):
			full_path = os.path.join(output_dir, file)
			with open(full_path, 'rb') as f:
				data = pickle.load(f)
				data_b.append(data)

	if datatype=="one_hot" or datatype=="boolean" or datatype=="integers":
		data_a = np.stack(data_a)
		data_b = np.stack(data_b)
		data = np.concatenate((data_a, data_b), axis=1)
		data = np.sum(data, axis=0)
		return data
	elif datatype=="rankings":
		data_a = np.stack(data_a)
		data_b = np.stack(data_b)
		data = np.concatenate((data_a, data_b), axis=1)
		data = np.mean(data, axis=0)
		return data
	else:
		raise Exception("Incorrect datatype!") 

def run_through_dataset(data, datatype, local_mechanism_object, output_dir):
	allowed_datatypes = ["one_hot", "boolean", "integers", "rankings"]
	if datatype not in allowed_datatypes:
		raise ValueError(f"Invalid datatype '{datatype}'. Allowed datatypes are: {allowed_datatypes}")
	for user_id, user in enumerate(tqdm(data, desc="completing_local_dp")):
		user = deepcopy(user)
		user = local_mechanism_object.randomize(user, datatype)
		# splitting
		split_a, split_b = user[:int(len(user)//2)], user[int(len(user)//2):]
		communicate(split_a, split_b, output_dir, user_id)
	return aggregate_from_output_dir(output_dir, datatype)

def app():
	st.title("Locational DP Framework")

	with st.form(key='dp_form'):
		epsilon = st.slider('Select the privacy parameter ε', min_value=1.0, max_value=10.0, value=1.0, step=0.5)
		st.write("Selected ε value:", epsilon)
		col1, col2 = st.columns(2)
		with col1:
			datatype = st.selectbox("Select the data type", ["One Hot Encoded (Apple's Example)", "Boolean (Contagion Tracking)", "Integers (Income)", "Rankings (Elections)"])
			st.write("You selected the data type:", datatype)
		with col2:
			mechanism = st.selectbox("Select the privacy mechanism", ["Randomized Response", "Exponential Mechanism", "Gaussian Mechanism"])
			st.write("You selected the mechanism:", mechanism)
		submit_button = st.form_submit_button(label='Apply Privacy Mechanism')

	if submit_button:
		if mechanism=="Gaussian Mechanism":
			delta = 1e-3
			st.write("Applying", mechanism, "to", datatype, "with ε =", epsilon, "with δ =", delta)
		else:
			st.write("Applying", mechanism, "to", datatype, "with ε =", epsilon)

		ohs = OneHotSimulator()
		_, width, height = ohs.terrain_map.shape
		if datatype=="One Hot Encoded (Apple's Example)":
			data_obj = OneHotSimulator()
			dataset = []
			for i in range(5):
				data = data_obj.get_experimental_instance(0)
				data = clean_one_hot(data, width, height)
				dataset.append(data)
			data_type = "one_hot"
			if mechanism=="Randomized Response":
				local_dp_obj = RandomizedResponse(epsilon, max_income=60000)
				local_dp_path = "rr"
			elif mechanism=="Exponential Mechanism":
				local_dp_obj = ExponentialMechanism(epsilon, max_income=60000)
				local_dp_path = "em"
			else:
				local_dp_obj = GaussianMechanism(epsilon, delta=delta, max_income=max_income)
				local_dp_path = "gm"
			outputs = []
			for data in dataset:
				output = run_through_dataset(data, data_type, local_dp_obj, "./output/"+data_type+"/"+local_dp_path+"/")
				outputs.append(output)
			outputs = np.array(outputs)
			outputs = outputs/np.sum(outputs, axis=0)
			stringed_outputs = []
			features = ["Sky", "People", "Path", "Bridge", "Sunset"]
			for i in range(outputs.shape[1]):
				string = ""
				for j in range(outputs.shape[0]):
					string += str(j+1)+". "+features[j]+"\t"+str(round(100*float(outputs[j][i]), 1))+"%\n"
				string = string[:-1]
				stringed_outputs.append(string)
			output = np.array(stringed_outputs)
			output = output.reshape((width, height))
			midpoint = 40.4432, -79.9428
			diff_range = 0.02, 0.05
			diff_steps = diff_range[0]/output.shape[0], diff_range[1]/output.shape[1]
			top_point = midpoint[0]+((output.shape[0]//2)*diff_steps[0]), midpoint[1]-((output.shape[1]//2)*diff_steps[1])
			df = []
			for i in range(output.shape[0]):
				for j in range(output.shape[1]):
					dictionary = {"x": top_point[0]-diff_steps[0]*i, "y": top_point[1]+diff_steps[1]*j, "value": output[i][j]}
					df.append(dictionary)
			df = pd.DataFrame(df)
			df = df.values
			main_map = make_map(df, diff_steps)
			folium_static(main_map)
		else:
			if datatype=="Boolean (Contagion Tracking)":
				data_obj = BooleanSimulator()
				data = data_obj.get_experimental_instance()
				data = clean_boolean(data, width, height)
				data_type = "boolean"
			elif datatype=="Integers (Income)":
				data_obj = IntegerSimulator()
				data = data_obj.get_experimental_instance()
				data = clean_integers(data, width, height)	
				data_type = "integers"
			else:
				data_obj = RankingsSimulator()
				data = data_obj.get_experimental_instance(0)
				data = clean_rankings(data, width, height)
				data_type = "rankings"

			if mechanism=="Randomized Response":
				local_dp_obj = RandomizedResponse(epsilon, max_income=60000)
				local_dp_path = "rr"
			elif mechanism=="Exponential Mechanism":
				local_dp_obj = ExponentialMechanism(epsilon, max_income=60000)
				local_dp_path = "em"
			else:
				local_dp_obj = GaussianMechanism(epsilon, delta=delta, max_income=max_income)
				local_dp_path = "gm"

			output = run_through_dataset(data, data_type, local_dp_obj, "./output/"+data_type+"/"+local_dp_path+"/")
			output /= output.shape[0]
			if data_type=="rankings":
				output = np.argmax(output, axis=1)
			output = output.reshape((width, height))
			midpoint = 40.4432, -79.9428
			diff_range = 0.02, 0.05
			diff_steps = diff_range[0]/output.shape[0], diff_range[1]/output.shape[1]
			top_point = midpoint[0]+((output.shape[0]//2)*diff_steps[0]), midpoint[1]-((output.shape[1]//2)*diff_steps[1])
			df = []
			for i in range(output.shape[0]):
				for j in range(output.shape[1]):
					dictionary = {"x": top_point[0]-diff_steps[0]*i, "y": top_point[1]+diff_steps[1]*j, "value": output[i][j]}
					df.append(dictionary)
			df = pd.DataFrame(df)
			df = df.values
			main_map = make_map(df, diff_steps)
			folium_static(main_map)

if __name__ == '__main__':
	app()
	