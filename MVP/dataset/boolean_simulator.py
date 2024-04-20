from .base_simulator import main as terrain_generator
import numpy as np
from tqdm import trange

class BooleanSimulator:
	def __init__(self, user_min=0.05, user_max=0.15, num_clients=1000, seed=0):
		np.random.seed(seed)
		assert 0<user_min<1 and 0<user_max<1, "Wrong % Values for Boolean"
		self.seed = seed
		self.num_clients = num_clients
		self.terrain_map = self.generate_map()
		self.user_min = int(self.terrain_map.shape[1]*user_min)
		self.user_max = int(self.terrain_map.shape[1]*user_max)
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
			random_indices = indices_above_half[np.random.choice(indices_above_half.shape[0], replace=False, size=np.random.randint(self.user_min, self.user_max))]
			data.append(random_indices)
		return data

	def get_experimental_instance(self):
		return self.data

if __name__ == '__main__':
	bs = BooleanSimulator()
	data = bs.get_experimental_instance()
	print(data[:3], len(data), len(data[0]), len(data[0][0]))