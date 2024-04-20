import numpy as np

class GaussianMechanism:
	def __init__(self, epsilon, delta, max_income):
		self.max_income = max_income
		self.epsilon = epsilon
		self.delta = delta

	def randomize_one_hot(self, data, sigma=None):
		if sigma is None:
			sigma = np.sqrt(2 * np.log(1.25 / self.delta)) * (1 / self.epsilon)
		noisy_scores = data + np.random.normal(loc=0.0, scale=sigma, size=data.shape)
		noisy_scores[noisy_scores>0.5] = 1
		noisy_scores[noisy_scores<=0.5] = 0
		return noisy_scores

	def randomize_boolean(self, data):
		sigma = np.sqrt(2 * np.log(1.25 / self.delta)) * (1 / self.epsilon) * np.sqrt(len(data))
		return self.randomize_one_hot(data, sigma=sigma)

	def randomize_rankings(self, data, sigma=None):
		if sigma is None:
			sigma = np.sqrt(2 * np.log(1.25 / self.delta)) * (1 / self.epsilon)
		compressed_data = np.mean(data, axis=1)
		zeros_np = np.zeros_like(compressed_data)
		index = np.argwhere(compressed_data>0)[0][0]
		zeros_np[compressed_data>0] = 1
		noisy_scores = zeros_np + np.random.normal(loc=0.0, scale=sigma, size=zeros_np.shape)
		data_ = np.zeros_like(data)
		data_[np.argmax(noisy_scores)] = data[index]
		return data_

	def randomize_integers(self, data, sigma=None):
		if sigma is None:
			sigma = np.sqrt(2 * np.log(1.25 / self.delta)) * (self.max_income / self.epsilon)
		zeros_np = np.zeros_like(data)
		index = np.argwhere(data>0)[0][0]
		zeros_np[data>0] = 1
		noisy_scores = zeros_np + np.random.normal(loc=0.0, scale=sigma, size=zeros_np.shape)
		data_ = np.zeros_like(data)
		data_[np.argmax(noisy_scores)] = data[index]
		return data_

	def randomize(self, data, datatype):
		if datatype=="one_hot":
			return self.randomize_one_hot(data)
		elif datatype=="boolean":
			return self.randomize_boolean(data)
		elif datatype=="integers":
			return self.randomize_integers(data)
		elif datatype=="rankings":
			return self.randomize_rankings(data)
		else:
			raise Exception("Unknown datatype!")
