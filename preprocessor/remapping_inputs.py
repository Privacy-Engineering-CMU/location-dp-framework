import numpy as np

def clean_one_hot(data, w, h):
	d = []
	for user in data:
		per_user_vector = np.zeros(h*w)
		index = user[0]*h + user[1]
		per_user_vector[index] = 1
		d.append(per_user_vector)
	d = np.stack(d)
	return d

def clean_boolean(data, w, h):
	d = []
	for user in data:
		per_user_vector = np.zeros(h*w)
		for u in user:
			index = u[0]*h + u[1]
			per_user_vector[index] = 1
		d.append(per_user_vector)
	d = np.stack(d)
	return d

def clean_rankings(data, w, h, ranking_dim=5):
	d = []
	for user in data:
		per_user_vector = np.zeros((h*w, ranking_dim))
		index = user[0]*h + user[1]
		per_user_vector[index] = user[2:]
		d.append(per_user_vector)
	d = np.stack(d)
	return d

def clean_integers(data, w, h):
	d = []
	for user in data:
		per_user_vector = np.zeros(h*w)
		index = user[0]*h + user[1]
		per_user_vector[index] = user[2]
		d.append(per_user_vector)
	d = np.stack(d)
	return d