from dataset import *
from preprocessor import *

def main():
	ohs = OneHotSimulator()
	_, width, height = ohs.terrain_map.shape

	data = ohs.get_experimental_instance(0)
	data = clean_one_hot(data, width, height)
	print(data.shape)

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
	