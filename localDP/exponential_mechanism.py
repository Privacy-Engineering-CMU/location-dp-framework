import numpy as np

class ExponentialMechanism:
	def __init__(self, epsilon, max_income):
		self.max_income = max_income
		self.epsilon = epsilon

	def randomize_one_hot(self, data, scale=None):
		if scale is None:
			scale = 1/self.epsilon
		noisy_scores = data + np.random.laplace(loc=0.0, scale=scale, size=data.shape)
		noisy_scores[noisy_scores>0.5] = 1
		noisy_scores[noisy_scores<=0.5] = 0
		return noisy_scores

	def randomize_boolean(self, data):
		scale = len(data)/self.epsilon
		return self.randomize_one_hot(data, scale=scale)

	def randomize_rankings(self, data, scale=None):
		if scale is None:
			scale = 1/self.epsilon
		compressed_data = np.mean(data, axis=1)
		zeros_np = np.zeros_like(compressed_data)
		index = np.argwhere(compressed_data>0)[0][0]
		zeros_np[compressed_data>0] = 1
		noisy_scores = zeros_np + np.random.laplace(loc=0.0, scale=scale, size=zeros_np.shape)
		data_ = np.zeros_like(data)
		data_[np.argmax(noisy_scores)] = data[index]
		return data_

	def randomize_integers(self, data, scale=None):
		if scale is None:
			scale = 1/self.epsilon
		zeros_np = np.zeros_like(data)
		index = np.argwhere(data>0)[0][0]
		zeros_np[data>0] = 1
		noisy_scores = zeros_np + np.random.laplace(loc=0.0, scale=scale, size=zeros_np.shape)
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
