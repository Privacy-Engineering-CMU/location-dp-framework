import numpy as np
import random

class DatasetGenerator:
    def __init__(self, n=10, pincode_lower=15100, pincode_upper=15300, object_cnt=10, rating=5):
        """
        Initializes the DatasetGenerator with default parameters.

        Parameters:
            n (int, optional): Number of data points to generate. Default is 10.
            pincode_lower (int, optional): Lower bound of zip code range. Default is 15100.
            pincode_upper (int, optional): Upper bound of zip code range. Default is 15300.
            object_cnt (int, optional): Number of objects/features in each data point. Default is 10.
            rating (int, optional): Maximum rating value for type 4 dataset. Default is 5.
        """
        self.n = n
        self.pincode_lower = pincode_lower
        self.pincode_upper = pincode_upper
        self.object_cnt = object_cnt
        self.rating = rating

    def generate_dataset(self, gen_type):
        """
        Generates a dataset of different types based on the provided generation type.

        Parameters:
            gen_type (int): Type of dataset to generate.
                1: Zip Code, Binary (one-hot)
                2: Zip Code, Binary (boolean)
                3: Zip Code, Integers
                4: Zip Code, Rating (Categorical/Ordinal)

        Returns:
            list: List of tuples where each tuple contains a zip code and its corresponding data point based on the specified generation type.
        """
        zip_codes = np.linspace(self.pincode_lower, self.pincode_upper, self.n, dtype=int)
        random.shuffle(zip_codes)

        if gen_type == 1:
            data = np.eye(self.object_cnt, dtype=int)[np.random.choice(self.object_cnt, self.n)]
        elif gen_type == 2:
            data = np.random.randint(2, size=(self.n, self.pincode_upper-self.pincode_lower), dtype=bool)
        elif gen_type == 3:
            data = np.random.randint(1, self.object_cnt+1, size=(self.n, self.object_cnt), dtype=int)
        elif gen_type == 4:
            data = np.random.randint(1, self.rating+1, size=self.n)

        data_with_zipcodes = list(zip(zip_codes, data))

        return data_with_zipcodes

# Example usage:
# Create an instance of DatasetGenerator
generator = DatasetGenerator()

# Generate a dataset of type 1 (Zip Code, Binary - one-hot)
dataset_type_1 = generator.generate_dataset(gen_type=1)

# Generate a dataset of type 2 (Zip Code, Binary - boolean)
dataset_type_2 = generator.generate_dataset(gen_type=2)

# Generate a dataset of type 3 (Zip Code, Integers)
dataset_type_3 = generator.generate_dataset(gen_type=3)

# Generate a dataset of type 4 (Zip Code, Rating - Categorical/Ordinal)
dataset_type_4 = generator.generate_dataset(gen_type=4)
