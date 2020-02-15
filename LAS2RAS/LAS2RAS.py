### Copy and paste this script into the ArcMap Python terminal.
### If you have any questions, ask Jonny Norwine. 

import arcpy
 
### SETUP ############################################

# full path of the folder where you want to save .lasd file 
# USE DOUBLE BACKSLASH AND END WITH DOUBLE BACKSLASH
# e.g. "E:\\jnorwine\\ArcMap\\Rifts\\"
lasd_output_path = "E:\\Caitlin\\PIPERS\\LiDAR_LAS_Dataset\\"
raster_output_path = "E:\\Caitlin\\PIPERS\\LiDAR_Rasters\\"


# full path of the geodatabase where you want to save the raster
# USE DOUBLE BACKSLASH AND END WITH DOUBLE BACKSLASH
# e.g. "E:\\jnorwine\\ArcMap\\Rifts\\ROSETTA_Rifts.gdb\\"
output_gdb_path = "E:\\Caitlin\\ROSETTA\\ROSETTA Database\\ROSETTA.gdb\\"


# las_array is a list of lists, where each inner list represents one raster 
# las_array = [["output filename", "input file path", "input file path", ...],
#              ["output filename," "input file path", "input file path", ...]
#               ...                                                    ...  ]
las_array = [["AN03_F1004_1","X:\\trunk\\icepod\\antarctica\\20162017\\lidar\\vq580\\pointcloud\\F1004\\las\\full_swath\AN03_F1004_20161127_204658_LIDAR_VQ580_Record1.las"]]

#######################################################
    
for las_list in las_array:
 
     name = las_list[0]
     path_list = las_list[1:]
     
     arcpy.CreateLasDataset_management(path_list, lasd_output_path + name + ".lasd", "NO_RECURSION", "", arcpy.SpatialReference(4326), "COMPUTE_STATS", "RELATIVE_PATHS", "NO_FILES")
     
     arcpy.LasDatasetToRaster_conversion(lasd_output_path + name + ".lasd", output_gdb_path + name, "ELEVATION", 'BINNING AVERAGE SIMPLE', 'FLOAT', 'CELLSIZE', 0.00001, 1)

     #arcpy.RasterToOtherFormat_conversion(output_gdb_path + name, raster_output_path, {"TIFF"})