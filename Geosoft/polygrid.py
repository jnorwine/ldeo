import sys
import os 
import numpy as np 
import pandas as pd

### CONFIG ####################

output = "F:\\jnorwine\\polygrid-test\\"

min_x = -520839.356282419
max_x = 379525.96847538871
min_y = -1378805.442002085
max_y = -516969.2640244537

x_overlap = 0.5 
y_overlap = 0.5

overshoot = True # if True, boxes will extend beyond the bounds set above to cover the whole area

cell_width = 110e3
cell_height = 110e3

header = "/#CoordinateSystem=\"WGS 84 / *EPSG3031\"\n/#Datum=\"WGS 84\",6378137,0.0818191908426215,0\n/#Projection=\"Polar Stereographic\",-90,0,0.9728,0,0\n/#Units=m,1\n/#LocalDatum=\"WGS 84\",0,0,0,0,0,0,0\npoly 1\n" 

###############################

folder_path = os.path.join(output, "polygrid\\")
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# set up array of bounds
xlist = []
ylist = []

x = min_x 
y = min_y 

while x < max_x:
    xlist.append(x)
    x += (1 - x_overlap) * cell_width 
    
while y < max_y:
    ylist.append(y)
    y += (1 - y_overlap) * cell_height

array = []
for y_idx in range(len(ylist) - 2):
    row = []
    for x_idx in range(len(xlist) - 2):
        new_min_x = xlist[x_idx]
        new_max_x = xlist[x_idx + 2]
        new_min_y = ylist[y_idx]
        new_max_y = ylist[y_idx + 2]

        row.append([new_min_x, new_max_x, new_min_y, new_max_y])
    array.insert(0, row) 

# array[] selects row in grid
# array[][] selects box in row 
# array[][][] selects point in box: [xmin, xmax, ymin, ymax] 

row_num = 0
box_num = 0

for row in array:
    box_num = 0
    for box in row: 
        with open(folder_path + "row" + str(row_num) + "_box" + str(box_num) + ".ply", "w") as file:
            
            file.write(header)
            file.write("              " + str(box[0]) + "              " + str(box[2]) + "\n") # bottom left
            file.write("              " + str(box[1]) + "              " + str(box[2]) + "\n") # bottom right 
            file.write("              " + str(box[1]) + "              " + str(box[3]) + "\n") # top right 
            file.write("              " + str(box[0]) + "              " + str(box[3]) + "\n") # top left 
            
            box_num += 1 
            
    row_num += 1         
            
            