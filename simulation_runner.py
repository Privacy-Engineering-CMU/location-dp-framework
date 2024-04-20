from dataset import *
from preprocessor import *
from localDP import *
from tqdm import tqdm
import pickle
import os

def communicate(a, b, output_dir, user_id):
	os.makedirs(output_dir, exist_ok=True)
	file_path_a = os.path.join(output_dir, f"user_{user_id}_a.pkl")
	file_path_b = os.path.join(output_dir, f"user_{user_id}_b.pkl")
	with open(file_path_a, 'wb') as file_a:
		pickle.dump(a, file_a)
	with open(file_path_b, 'wb') as file_b:
		pickle.dump(b, file_b)

def aggregate_from_output_dir(output_dir, datatype):
	pass
	print(output_dir)
	exit()

def run_through_dataset(data, datatype, local_mechanism_object, output_dir):
	allowed_datatypes = ["one_hot", "boolean", "integers", "rankings"]
	if datatype not in allowed_datatypes:
		raise ValueError(f"Invalid datatype '{datatype}'. Allowed datatypes are: {allowed_datatypes}")
	for user_id, user in enumerate(tqdm(data, desc="completing_local_dp")):
		user = local_mechanism_object.randomize(user, datatype)
		# splitting
		split_a, split_b = user[:int(len(user)//2)], user[int(len(user)//2):]
		communicate(split_a, split_b, output_dir, user_id)
	aggregate_from_output_dir(output_dir, datatype)
	

def main():
	rr = RandomizedResponse(1)

	ohs = OneHotSimulator()
	_, width, height = ohs.terrain_map.shape

	data = ohs.get_experimental_instance(0)
	data = clean_one_hot(data, width, height)
	run_through_dataset(data, "one_hot", rr, "./output/one_hot/rr/")
	exit()

	bs = BooleanSimulator()
	data = bs.get_experimental_instance()
	data = clean_boolean(data, width, height)
	print(data.shape)

	rs = RankingsSimulator()
	data = rs.get_experimental_instance(0)
	data = clean_rankings(data, width, height)
	print(data.shape)

	i_s = IntegerSimulator()
	data = i_s.get_experimental_instance()
	data = clean_integers(data, width, height)
	print(data.shape)

if __name__ == '__main__':
	main()
	