### Copy and paste this script into the ArcMap Python terminal.
### Created by Jonny Norwine in 2019.
### Last updated:

import arcpy
import os
import re

### SETUP ############################################

# full path of the folder where you want to save .lasd file
# USE DOUBLE BACKSLASH AND END WITH DOUBLE BACKSLASH
# e.g. "E:\\jnorwine\\ArcMap\\Rifts\\"
#
lasd_output_path = "E:\\Caitlin\\PIPERS\\LiDAR_LAS_Dataset\\"
raster_output_path = "E:\\Caitlin\\PIPERS\\LiDAR_Rasters\\"


# full path of the geodatabase where you want to save the raster
# USE DOUBLE BACKSLASH AND END WITH DOUBLE BACKSLASH
# e.g. "E:\\jnorwine\\ArcMap\\Rifts\\ROSETTA_Rifts.gdb\\"
#
output_gdb_path = "E:\\Caitlin\\ROSETTA\\ROSETTA Database\\ROSETTA.gdb\\"

# path to folder of record files
#
input_folder = "C:\\Users\\caitlin\\Desktop\\AN03_F1004\\"

#######################################################

file_list = next(os.walk(input_folder))[2]
new_file_list = []

for file_name in file_list:
    result = re.search(r"\.las$", file_name)
    if result != None:
        new_file_list.append(file_name)

file_list = new_file_list

conflict = 0
for file in file_list:
        name = re.search(r"(.+)\.", file).group(1)
        if os.path.exists(lasd_output_path + name + ".lasd"):
            conflict = 1
            break

if conflict == 1:
    print("Some of the output files already exist.")
    print("[1] Skip these files")
    #print("[2] Overwrite these files")
    print("[2] Keep both files")
    dup_response = input()
    if dup_response == "1":
        pass
    # elif dup_response == "2":
    #     pass
    elif dup_response == "2":
        pass
    else:
        print("Invalid response. Respond with 1 or 2.")
        dup_response = input()

prog = 0
for file in file_list:

    prog += 1
    print("working on " + file + "(" + str(prog) + "/" + str(len(file_list)) + ")" + "...")
    name = re.search(r"(.+)\.", file).group(1)
    path_list = [os.path.join(input_folder, file)]

    try:
        arcpy.CreateLasDataset_management(path_list, lasd_output_path + name + ".lasd", "NO_RECURSION", "", arcpy.SpatialReference(4326), "COMPUTE_STATS", "RELATIVE_PATHS", "NO_FILES")
        arcpy.LasDatasetToRaster_conversion(lasd_output_path + name + ".lasd", output_gdb_path + name, "ELEVATION", 'BINNING AVERAGE SIMPLE', 'FLOAT', 'CELLSIZE', 0.00001, 1)
    except:
        if dup_response == "1":
            pass
        elif dup_response == "2":
            arcpy.CreateLasDataset_management(path_list, lasd_output_path + name "_1" + ".lasd", "NO_RECURSION", "", arcpy.SpatialReference(4326), "COMPUTE_STATS", "RELATIVE_PATHS", "NO_FILES")
            arcpy.LasDatasetToRaster_conversion(lasd_output_path + name + "_1" + ".lasd", output_gdb_path + name, "ELEVATION", 'BINNING AVERAGE SIMPLE', 'FLOAT', 'CELLSIZE', 0.00001, 1)

     arcpy.RasterToOtherFormat_conversion(output_gdb_path + name, raster_output_path, "TIFF")
