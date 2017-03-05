import numpy as np
import math
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

if __name__=="__main__":
	fuse_file = open('final_project_data/final_project_point_cloud.fuse', 'rb')
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
	
	print "Lat length: " + len(lat_set)
	print "Long length: " + len(long_set)
	print "Lat min: " + min(lat_set)
	print "Long min: " + min(long_set)
	print "Lat max: " + max(lat_set)
	print "Long max: " + max(long_set)