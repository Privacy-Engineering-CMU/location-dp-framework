import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt

# Function to calculate distance between latitudes and longitudes
def calculate_distance(coord1, coord2):
    # Assuming a flat earth model for simplicity in a small geographic area
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def main(seed):
    # Pittsburgh Coordinates dictionary
    coordinates = {
        "Top Right": (40.495857, -79.875791),
        "Bottom Right": (40.366759, -79.875791),
        "Top Left": (40.495857, -80.106503),
        "Bottom Left": (40.366759, -80.106503)
    }

    # Calculate widths and heights in terms of degrees
    width = calculate_distance(coordinates["Top Right"], coordinates["Top Left"])
    height = calculate_distance(coordinates["Top Right"], coordinates["Bottom Right"])

    # Define the grid size for the heatmap
    grid_width = int(width * 100)  # scale factor to get a reasonable number of points
    grid_height = int(height * 100)

    # Generate Perlin noise-based terrain data
    noise = PerlinNoise(octaves=4, seed=seed)
    terrain = np.array([[noise([i/grid_height, j/grid_width]) for j in range(grid_width)] for i in range(grid_height)])

    # Normalize the terrain values to be between 0 and 1
    terrain = (terrain - terrain.min()) / (terrain.max() - terrain.min())
    return np.square(terrain)

if __name__ == '__main__':
    terrain = main(0)
    print(np.mean(terrain), np.std(terrain))
    plt.imshow(terrain)
    plt.show()