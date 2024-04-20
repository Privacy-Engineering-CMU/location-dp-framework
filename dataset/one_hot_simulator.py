from .base_simulator import main as terrain_generator
import numpy as np
from tqdm import trange

class OneHotSimulator:
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
			user = []
			for feature_id in range(self.num_features):
				terrain = self.terrain_map[feature_id]
				indices_above_half = np.argwhere(terrain > np.mean(terrain)+np.std(terrain))
				if len(indices_above_half)<0:
					raise Exception("Invalid Simulation")
				random_index = indices_above_half[np.random.choice(indices_above_half.shape[0])]
				user.append(random_index)
			data.append(user)
		data = np.array(data)
		return data

	def get_experimental_instance(self, feature_id):
		if feature_id>=self.num_features:
			raise Exception("Feature ID isn't present!")
		return self.data[:, feature_id, :]

if __name__ == '__main__':
	ohs = OneHotSimulator()
	data = ohs.get_experimental_instance(0)
	print(data, data.shape)