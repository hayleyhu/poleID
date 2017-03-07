import pcl
import numpy as np
import math
import matplotlib.pyplot as plt 

p = pcl.PointCloud()
obj_file = open('point_cloud.obj', 'rb')
all_points = list()
for line in obj_file:
 point = line.strip().split(' ')
 all_points.append([float(point[1]),float(point[2]), float(point[3]) ])

all_points = np.array(all_points, dtype=np.float32)

p.from_array(all_points)
fil = p.make_statistical_outlier_filter()
fil.set_mean_k (5)
fil.set_std_dev_mul_thresh (1.0)
inliers = fil.filter()
#print "finish outlier filtering"
#print inliers

#Data Reduction
#Downsampling a PointCloud using a VoxelGrid filter

grid_filter = inliers.make_voxel_grid_filter()
grid_filter.set_leaf_size(0.1, 0.1, 0.1)
voxels = grid_filter.filter()
#print "finish voxel grid filtering"
"""
#Removing Planes
fil = voxels.make_passthrough_filter()
fil.set_filter_field_name("z")
fil.set_filter_limits(0, 4558020)
cloud_filtered = fil.filter()
"""
#print("finish cutting all things more than 12 meters")
#print cloud_filtered
"""
# Writing to obj
output_obj = open('cloud_filtered.obj', 'w')

for point in cloud_filtered:
    line = "v " + str(point[0]) + " " + str(point[1]) + " "+ str(point[2])+"\n"
    output_obj.write(line)

output_obj.close()
"""
seg = voxels.make_segmenter_normals(ksearch=50)
seg.set_optimize_coefficients(True)
seg.set_model_type(pcl.SACMODEL_NORMAL_PLANE)
seg.set_method_type(pcl.SAC_RANSAC)
seg.set_normal_distance_weight(0.1) 
seg.set_max_iterations(100)
seg.set_distance_threshold(0.1)
indices, model = seg.segment()


no_plane = voxels.extract(indices, negative=True)

print("finish cutting the plane")
print model
print no_plane

seg = no_plane.make_segmenter_normals(ksearch=50)
seg.set_optimize_coefficients(True)
seg.set_model_type(pcl.SACMODEL_CYLINDER)
seg.set_normal_distance_weight(0.1)
seg.set_method_type(pcl.SAC_RANSAC)
seg.set_max_iterations(1000)
seg.set_distance_threshold(1) 
seg.set_radius_limits(0, 5) 

segmented_indices, model = seg.segment()
print model 

#return just cylinder segments - FEATURE EXTRACTION
only_cylinder = no_plane.extract(segmented_indices, negative=False)
print "filtered cloud after only_cylinder"
print only_cylinder

# Writing to obj
output_obj = open('only_cylinder.obj', 'w')

for point in only_cylinder:
    line = "v " + str(point[0]) + " " + str(point[1]) + " "+ str(point[2])+"\n"
    output_obj.write(line)

output_obj.close()
