import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

import scipy.ndimage.filters as filters


def plot(data, title, save_path):
    colors = [(0, 0, 1), (0, 1, 1), (0, 1, 0.75), (0, 1, 0), (0.75, 1, 0),
              (1, 1, 0), (1, 0.8, 0), (1, 0.7, 0), (1, 0, 0)]

    cm = LinearSegmentedColormap.from_list('sample', colors)

    plt.imshow(data, cmap=cm)
    plt.colorbar()
    plt.title(title)
    plt.savefig(save_path)
    plt.close()

if __name__ == "__main__":
	obj_file = open('point_cloud.obj', 'rb')
	h = 1130
	w = 1960
	lat_min = 43639773
	long_min = 8504261
	data = np.zeros(h * w)
	data = data.reshape((h, w))

	for line in obj_file:
		r = line.strip().split(' ')
		x, y, z = float(r[1]) - lat_min, float(r[2]) - long_min, float(r[3])

		data[x][y] += 10
	
	plot(data, 'Sample plot', 'sample.png')