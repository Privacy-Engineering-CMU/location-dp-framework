from .base_simulator import main as terrain_generator
import numpy as np
from tqdm import trange
import pandas as pd

class IntegerSimulator:
	def __init__(self, num_clients=1000, seed=0, max_income=60000):
		self.max_income = max_income
		np.random.seed(seed)
		self.seed = seed
		self.num_clients = num_clients
		self.terrain_map = self.generate_map()
		self.data = self.generate_data()

	def generate_map(self):
		return terrain_generator(self.seed)

	def generate_data(self):
		data = []
		for user_id in trange(self.num_clients, desc="simulating_users"):
			terrain = self.terrain_map
			indices_above_half = np.argwhere(terrain > np.mean(terrain)+np.std(terrain))
			if len(indices_above_half)<0:
				raise Exception("Invalid Simulation")
			random_indices = indices_above_half[np.random.choice(indices_above_half.shape[0])]
			income = int(self.max_income*np.sqrt(terrain[random_indices[0], random_indices[1]]))
			data.append({"zip_code_0":random_indices[0], "zip_code_1":random_indices[1], "integer": income})
		data = pd.DataFrame(data)
		data = data.values
		return data

	def get_experimental_instance(self):
		return self.data

if __name__ == '__main__':
	i_s = IntegerSimulator()
	data = i_s.get_experimental_instance()
	print(data[:3], data.shape)