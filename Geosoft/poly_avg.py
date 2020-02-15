import re
import os
import geosoft.gxapi as gxapi
import numpy as np
import pandas as pd
import geosoft.gxpy as gxpy
from tqdm import tqdm
import sys

ply_folder = "G:\\jnorwine\\polygrid-test\\polygrid\\"
scratch_path = "G:\\jnorwine\\polygrid-test\\polygrid\\scratch.gs"
scratch_grid_path = "G:\\jnorwine\\Python Geosoft\\scratch.grd"
grid_path = "G:\\jnorwine\\rosetta - Copy\\Werner\\RIS_werner_cluster_2_1000_5k_full.grd"
out_csv_path = "G:\\jnorwine\\Python Geosoft\\werner_ply_avg.csv"

def write_window_gs(ply_path, in_grd_path, out_grd_path, scratch_path):

    gs = (
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG OPENED : Wed Jul 03 13:12:38 2019\n"
    f"/-------------------------------------------------------------------------\n"
    f"SETINI         GRIDMASK.GRDIN=\"{in_grd_path}\"\n"
    f"SETINI         GRIDMASK.GRDOUT=\"{out_grd_path}\"\n"
    f"SETINI         GRIDMASK.POLY=\"{ply_path}\"\n"
    f"SETINI         GRIDMASK.MASKOPT=\"OUTSIDE\"\n"
    f"SETINI         GRIDMASK.RESIZE=\"YES\"\n"
    f"GX             gridmask.gx\n"
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG CLOSED : Wed Jul 03 13:14:07 2019\n"
    f"/-------------------------------------------------------------------------\n"
    )

    with open(scratch_path, "w") as file:
        file.write(gs)

def rungx():

    try:
        os.remove(scratch_path)
    except:
        pass

    try:
        os.remove(scratch_path + ".xml")
    except:
        pass

    try:
        os.remove(scratch_path + ".gi")
    except:
        pass

    try:
        os.remove(scratch_grid_path)
    except:
        pass

    ply_list = next(os.walk(ply_folder))[2]
    center_x_list = []
    center_y_list = []
    avg_list = []

    try:
        gxapi.GXSYS.set_interactive(0)
    except:
        print("Unable to set_interactive, restart Geosoft and try again.")
        input("Press any key to exit...")
        sys.exit()

    for ply in tqdm(ply_list, ascii=True):

        ply_path = os.path.join(ply_folder, ply)
        f = open(ply_path)

        lines = []
        for line in f:
            lines.append(line)

        try:
            xmin, ymin = re.findall(r"\s+([\w.-]+)\s+([\w.-]+)\n", lines[6])[0]
            xmax, ymax = re.findall(r"\s+([\w.-]+)\s+([\w.-]+)\n", lines[8])[0]
        except:
            print("problem reading " + ply)
            input("press enter to exit...")
            sys.exit()
        xmin = float(xmin)
        xmax = float(xmax)
        ymin = float(ymin)
        ymax = float(ymax)

        dx = xmax - xmin
        dy = ymax - ymin

        center_x = xmin + 0.5*dx
        center_y = ymin + 0.5*dy
        center_x_list.append(center_x)
        center_y_list.append(center_y)

        write_window_gs(ply_path, grid_path, scratch_grid_path, scratch_path)
        gxapi.GXSYS.run_gs(scratch_path)

        with gxpy.grid.Grid.open(scratch_grid_path) as grid:
            grid_array = grid.np()
            avg = np.average(grid_array)
            avg_list.append(avg)

    df = pd.DataFrame()
    df["center_x"] = center_x_list
    df["center_y"] = center_y_list
    df["average"] = avg_list

    print(out_csv_path)
    print(df)
    input()

    # if not os.path.exists(out_csv_path):
    #     os.makedirs(out_csv_path)

    df.to_csv(out_csv_path, index=False)

    try:
        os.remove(scratch_path)
    except:
        pass

    try:
        os.remove(scratch_path + ".xml")
    except:
        pass

    try:
        os.remove(scratch_path + ".gi")
    except:
        pass

    try:
        os.remove(scratch_grid_path)
    except:
        pass
