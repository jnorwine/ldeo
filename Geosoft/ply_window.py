import geosoft.gxpy as gxpy
import geosoft.gxpy.project as gxproj
import geosoft.gxapi as gxapi
import os
from tqdm import tqdm
import re
import sys

# makes windowed grids out of all .ply files in a folder from an input grid

### CONFIG ##############################

ply_folder = "G:\\jnorwine\\polygrid-test\\polygrid\\"
write_path = "G:\\jnorwine\\polygrid-test\\polygrid\\scratch.gs" # path to .gs scratch file (needs to be empty or not exist yet)
in_grd_path = "G:\\jnorwine\\New Grav Grid\\merge_FA_imar2_SP_level_mask-regrid5km.grd"
output_folder = "G:\\jnorwine\\polygrid1\\windowed-grids\\gravity\\regrid5km"

#########################################

def write_window_gs(map_path, ply_path, in_grd_path, out_grd_path, write_path):

    gs = (
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG OPENED : Wed Jul 03 13:12:38 2019\n"
    f"/-------------------------------------------------------------------------\n"
    f"CURRENT        Map,\"{map_path}\"\n"
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

    with open(write_path, "w") as file:
        file.write(gs)

def rungx():

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    proj = gxproj.Geosoft_project()
    try:
        gxapi.GXSYS.set_interactive(0)
    except:
        print("Unable to set_interactive, restart Geosoft and try again.")
        input("Press any key to exit...")
        sys.exit()
    map_path = proj.current_map
    ply_list = next(os.walk(ply_folder))[2]

    for ply in tqdm(ply_list, ascii=True):
        try:
            ply_name = re.findall(r"(.*)\.ply", ply)[0]
        except:
            pass
        out_grd_path = os.path.join(output_folder, ply_name + ".grd(GRD)")
        ply_path = os.path.join(ply_folder, ply)
        write_window_gs(map_path, ply_path, in_grd_path, out_grd_path, write_path)
        gxapi.GXSYS.run_gs(write_path)

    os.remove(write_path)
