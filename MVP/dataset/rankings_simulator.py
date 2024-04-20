from .base_simulator import main as terrain_generator
import numpy as np
from tqdm import trange
from matplotlib import pyplot as plt
import pandas as pd

class RankingsSimulator:
	def __init__(self, num_features=5, num_clients=1000):
		self.num_features = num_features
		self.num_clients = num_clients
		self.terrain_map = self.generate_map()
		self.data = self.generate_data()

	def generate_map(self):
		terrains = []
		for seed in range(self.num_features):
			terrains.append(terrain_generator(seed))
		terrains = np.stack(terrains)
		return terrains

	def generate_data(self):
		data = []
		for user_id in trange(self.num_clients, desc="simulating_users"):
			all_indices = np.argwhere(self.terrain_map[0]>-1)
			random_zip_code = all_indices[np.random.choice(all_indices.shape[0])]
			ratings = np.argsort(self.terrain_map[:, random_zip_code[0], random_zip_code[1]])
			dictionary = {"zip_code_0":random_zip_code[0], "zip_code_1":random_zip_code[1]}
			dictionary_ = {"rating_"+str(i): ratings[i] for i in range(len(ratings))}
			dictionary.update(dictionary_)
			data.append(dictionary)
		data = pd.DataFrame(data)
		data =  data.values
		return data

	def get_experimental_instance(self, feature_id):
		return self.data

if __name__ == '__main__':
	rs = RankingsSimulator()
	data = rs.get_experimental_instance(0)
	print(data, data.shape)