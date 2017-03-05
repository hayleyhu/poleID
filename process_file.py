import numpy as np
import math
import matplotlib.pyplot as plt 

def LLHtoECEF(lat, lon, alt):
	lat = math.radians(lat)
	lon = math.radians(lon)
	# see http://www.mathworks.de/help/toolbox/aeroblks/llatoecefposition.html

	rad = np.float64(6378137.0)        # Radius of the Earth (in meters)
	f = np.float64(1.0/298.257223563)  # Flattening factor WGS84 Model
	cosLat = np.cos(lat)
	sinLat = np.sin(lat)
	FF     = (1.0-f)**2
	C      = 1/np.sqrt(cosLat**2 + FF * sinLat**2)
	S      = C * FF

	x = (rad * C + alt)*cosLat * np.cos(lon) // 0.1 
	y = (rad * C + alt)*cosLat * np.sin(lon) // 0.1
	z = (rad * S + alt)*sinLat // 0.1

	return (x, y, z)

def fuse2xyz(filename):
	fuse_file = open(filename, 'rb')
	point_info = list()
	lat_set = set()
	long_set = set()
	
	for line in fuse_file:
		r = line.strip().split(' ')
		point = []
		x, y, z = LLHtoECEF(float(r[0]), float(r[1]), float(r[2]))
		point.append(x)
		point.append(y)
		point.append(z)
		lat_set.add(x)
		long_set.add(y)
		point_info.append(point)

	obj_file = open('point_cloud.obj', 'w')
	
	for point in point_info:
		line = "v " + str(point[0]) + " " + str(point[1]) + " "+ str(point[2])
		obj_file.write(line)
		obj_file.write("\n")

	obj_file.close()


def intensityHistogram(filename):
	fuse_file = open(filename, 'rb')
	intens = list()
	for line in fuse_file:
		r = line.strip().split(' ')
		intensity = int(r[3])
		intens.append(intensity)

	intens = np.array(intens)
	mu = np.mean(intens)
	sigma = np.std(intens)
	n, bins, pathes = plt.hist(intens, bins=200, normed=1)
	plt.xlabel("Intensity")
	plt.ylabel('Probability')
	plt.grid(True)
	plt.show()

def filterIntensity(filename):
	fuse_file = open(filename, 'rb')
	point_info = list()
	for line in fuse_file:
		r = line.strip().split(' ')
		point = []
		intensity = int(r[3])
		if intensity>20 or intensity<2:
			continue
		x, y, z = LLHtoECEF(float(r[0]), float(r[1]), float(r[2]))
		point.append(x)
		point.append(y)
		point.append(z)
		point_info.append(point)

	obj_file = open('filtered_intensity_point_cloud.obj', 'w')

	for point in point_info:
		line = "v " + str(point[0]) + " " + str(point[1]) + " "+ str(point[2])
		obj_file.write(line)
		obj_file.write("\n")

	obj_file.close()

def centerPosition(xyzfilename):
	obj_file = open('filtered_intensity_point_cloud.obj', 'rb')
	xs = list()
	ys = list()
	for line in fuse_file:
		r = line.strip().split(' ')
		intensity = int(r[3])
		intens.append(intensity)

	intens = np.array(intens)
	mu = np.mean(intens)
	sigma = np.std(intens)
	n, bins, pathes = plt.hist(intens, bins=200, normed=1)
	plt.xlabel("Intensity")
	plt.ylabel('Probability')
	plt.grid(True)
	plt.show()


if __name__=="__main__":
	fuse_file = 'final_project_data/final_project_point_cloud.fuse'
	# intensityHistogram(fuse_file)
	filterIntensity(fuse_file)








	
=======
	
	print "Lat length: " + len(lat_set)
	print "Long length: " + len(long_set)
	print "Lat min: " + min(lat_set)
	print "Long min: " + min(long_set)
	print "Lat max: " + max(lat_set)
	print "Long max: " + max(long_set)
>>>>>>> 9d25bf0509ead8e70a35d1413d620d6a00a9097d
