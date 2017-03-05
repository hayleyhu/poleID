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

	x = (rad * C + alt)*cosLat * np.cos(lon) 
	y = (rad * C + alt)*cosLat * np.sin(lon) 
	z = (rad * S + alt)*sinLat 

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

def distanceToCenterHistogram():
	obj_file = open('filtered_intensity_point_cloud.obj', 'rb')
	xs = list()
	ys = list()
	coords = list()
	for line in obj_file:
		r = line.strip().split(' ')
		x = float(r[1])
		xs.append(x)
		y = float(r[2])
		ys.append(y)
		coords.append((x, y))
	obj_file.close()
	xs = np.array(xs)
	ys = np.array(ys)
	xmedian = np.median(xs)
	ymedian = np.median(ys)
	print xmedian, 
	print ymedian
	distances = list()

	for (x, y) in coords:

		dist = math.sqrt((x-xmedian)**2+(y-ymedian)**2)
		# print dist
		distances.append(dist)
	
	print distances[:30]
	distances = np.array(distances)
	mu = np.mean(distances)
	sigma = np.std(distances)
	n, bins, pathes = plt.hist(distances, bins=200, normed=1)
	plt.xlabel("Distances")
	plt.ylabel('Probability')
	plt.grid(True)
	plt.show()

def filterDistance(xmedian, ymedian):
	obj_file = open('filtered_intensity_point_cloud.obj', 'rb')
	point_info = list()
	for line in obj_file:
		r = line.strip().split(' ')
		point = []
		x = float(r[1])
		y = float(r[2])
		z = float(r[3])
		dist = math.sqrt((x-xmedian)**2+(y-ymedian)**2)
		if dist>40:
			continue
		point.append(x)
		point.append(y)
		point.append(z)
		point_info.append(point)

	outfile = open('filtered_intensity&distance_point_cloud.obj', 'w')

	for point in point_info:
		line = "v " + str(point[0]) + " " + str(point[1]) + " "+ str(point[2])
		outfile.write(line)
		outfile.write("\n")

	outfile.close()

if __name__=="__main__":
	fuse_file = 'final_project_data/final_project_point_cloud.fuse'
	# intensityHistogram(fuse_file)
	# filterIntensity(fuse_file)
	filterDistance(4364041.85813,850522.039477)







	

	
# 	print "Lat length: " + len(lat_set)
# 	print "Long length: " + len(long_set)
# 	print "Lat min: " + min(lat_set)
# 	print "Long min: " + min(long_set)
# 	print "Lat max: " + max(lat_set)
# 	print "Long max: " + max(long_set)
# >>>>>>> 9d25bf0509ead8e70a35d1413d620d6a00a9097d
