import geosoft.gxpy as gxpy
import geosoft.gxpy.project as gxproj
import geosoft.gxapi as gxapi
import os
from tqdm import tqdm

# draws all .ply files in input folder on current map

### CONFIG ##############################

input_folder = "G:\\jnorwine\\polygrid-test\\polygrid\\"
write_path = "G:\\jnorwine\\polygrid-test\\polygrid\\scratch.gs" # path to .gs scratch file (needs to be empty or not exist yet)

#########################################

def write_draw_gs(map_path, ply_path, write_path):

    gs = (
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG OPENED : Wed Jul 03 11:08:10 2019\n"
    f"/-------------------------------------------------------------------------\n"
    f"CURRENT        Map,\"{map_path}\"\n"
    f"SETINI         SCLMAP.GRID_SAVE=\"0\"\n"
    f"SETINI         SCLMAP.GRID_ONLY=\"0\"\n"
    f"SETINI         POLYDRAW.FILE=\"{ply_path}\"\n"
    f"SETINI         POLYDRAW.VIEW=\"Data\"\n"
    f"SETINI         POLYDRAW.NOCLIP=\"1\"\n"
    f"SETINI         POLYDRAW.POLYLINE=\"0\"\n"
    f"SETINI         POLYDRAW.POLYMULTI=\"0\"\n"
    f"SETINI         POLYDRAW.LINETHICK=\"0.15\"\n"
    f"SETINI         POLYDRAW.LINECOLOR=\"K\"\n"
    f"SETINI         POLYDRAW.FILLCOLOR=\"N\"\n"
    f"GX             polydraw.gx\n"
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG CLOSED : Wed Jul 03 11:08:43 2019\n"
    f"/-------------------------------------------------------------------------\n"
    )

    with open(write_path, "w") as file:
        file.write(gs)

def rungx():

    proj = gxproj.Geosoft_project()
    map_path = proj.current_map
    gxapi.GXSYS.set_interactive(0)
    ply_list = next(os.walk(input_folder))[2]

    for ply in tqdm(ply_list, ascii=True):

        ply_path = os.path.join(input_folder, ply)
        write_draw_gs(map_path, ply_path, write_path)
        gxapi.GXSYS.run_gs(write_path)

    os.remove(write_path)
