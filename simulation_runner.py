from dataset import *
from preprocessor import *
from localDP import *
from tqdm import tqdm
import pickle
import os
from copy import deepcopy

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
	
def main():
	epsilon = 1

	for local_dp_path, local_dp_obj in zip(["rr", "em", "gm"], [RandomizedResponse(epsilon, max_income=60000), ExponentialMechanism(epsilon, max_income=60000), GaussianMechanism(epsilon, delta=1e-3, max_income=60000)]):
		print(local_dp_path)

		ohs = OneHotSimulator()
		_, width, height = ohs.terrain_map.shape

		data = ohs.get_experimental_instance(0)
		data = clean_one_hot(data, width, height)
		output = run_through_dataset(data, "one_hot", local_dp_obj, "./output/one_hot/"+local_dp_path+"/")
		print(output)

		bs = BooleanSimulator()
		data = bs.get_experimental_instance()
		data = clean_boolean(data, width, height)
		output = run_through_dataset(data, "boolean", local_dp_obj, "./output/boolean/"+local_dp_path+"/")
		print(output)

		rs = RankingsSimulator()
		data = rs.get_experimental_instance(0)
		data = clean_rankings(data, width, height)
		output = run_through_dataset(data, "rankings", local_dp_obj, "./output/rankings/"+local_dp_path+"/")
		print(output)

		i_s = IntegerSimulator()
		data = i_s.get_experimental_instance()
		data = clean_integers(data, width, height)
		output = run_through_dataset(data, "integers", local_dp_obj, "./output/integers/"+local_dp_path+"/")
		print(output)
		print()

if __name__ == '__main__':
	main()
	