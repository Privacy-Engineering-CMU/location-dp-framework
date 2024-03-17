from simulation import BaseDatasetGenerator

def main(n=1000):
	dg = BaseDatasetGenerator(n)
	for gen_type in range(1, 5):
		data = dg.generate_dataset(gen_type)
		print(data)
		exit()
		print()


if __name__ == '__main__':
	main()