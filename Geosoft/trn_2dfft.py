import geosoft.gxpy as gxpy
import geosoft.gxpy.project as gxproj
import geosoft.gxapi as gxapi
import os
from tqdm import tqdm
import re

# makes windowed grids out of all .ply files in a folder from an input grid

### CONFIG ##############################

grd_folder = "G:\\jnorwine\\polygrid1\\windowed-grids\\gravity\\regrid5km\\"
write_path = "G:\\jnorwine\\polygrid-test\\polygrid\\scratch.gs" # path to .gs scratch file (needs to be empty or not exist yet)
output_folder = "G:\\jnorwine\\polygrid1\\trn_fft\\gravity\\regrid5km\\"

#########################################

def write_trn_gs(map_path, in_grd_path, out_trn_path, write_path):

    gs = (
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG OPENED : Wed Jul 03 16:40:35 2019\n"
    f"/-------------------------------------------------------------------------\n"
    f"CURRENT        Map,\"{map_path}\"\n"
    f"SETINI         FFT2IN.IN=\"{in_grd_path}\"\n"
    f"SETINI         FFT2FLT.IN=\"{out_trn_path}\"\n"
    f"SETINI         FFT2RSPC.TRN=\"{out_trn_path}\"\n"
    f"SETINI         FFT2PSPC.TRN=\"{out_trn_path}\"\n"
    f"GX             fft2in.gx\n"
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG CLOSED : Wed Jul 03 16:40:58 2019\n"
    f"/-------------------------------------------------------------------------\n"
    )

    with open(write_path, "w") as file:
        file.write(gs)

def write_fft_gs(map_path, in_trn_path, out_grd_path, write_path):

    gs = (
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG OPENED : Wed Jul 03 17:06:13 2019\n"
    f"/-------------------------------------------------------------------------\n"
    f"CURRENT        Map,\"{map_path}\"\n"
    f"SETINI         FFT2PSPC.TRN=\"{in_trn_path}\"\n"
    f"SETINI         FFT2PSPC.SPC=\"{out_grd_path}\"\n"
    f"GX             fft2pspc.gx\n"
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG CLOSED : Wed Jul 03 17:06:42 2019\n"
    f"/-------------------------------------------------------------------------\n"
    )

    with open(write_path, "w") as file:
        file.write(gs)

def rungx():

    trn_path_list = []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    proj = gxproj.Geosoft_project()
    gxapi.GXSYS.set_interactive(0)
    map_path = proj.current_map
    grd_list = next(os.walk(grd_folder))[2]

    # filter grd_list to only include .grd files
    for path in grd_list: # for some reason this does not catch .grd.xml
        if not path.endswith(".grd"):
            grd_list.remove(path)
            #print("removed " + path)

    for path in grd_list: # for some reason this does not catch .grd.gi
        newpath = path
        if not path.endswith(".grd"):
            grd_list.remove(path)
            #print("removed " + path)

    #input(grd_list)

    print("creating transfer files")
    for grd in tqdm(grd_list, ascii=True):

        grd_name = re.findall(r"(.*)\.grd", grd)[0]
        out_trn_path = os.path.join(".\\\\", grd_name + "_trn" + ".grd(GRD;TYPE=FLOAT)")
        in_grd_path = os.path.join(grd_folder, grd)
        write_trn_gs(map_path, in_grd_path, out_trn_path, write_path)
        gxapi.GXSYS.run_gs(write_path)
        trn_path_list.append(out_trn_path)

    print("performing FFT")
    for trn_path in tqdm(trn_path_list, ascii=True):

        trn_name = re.findall(r".*\\(.+)\.grd", trn_path)[0]
        out_grd_path = os.path.join(output_folder, trn_name + "_output" + ".grd(GRD)")
        write_fft_gs(map_path, trn_path, out_grd_path, write_path)
        gxapi.GXSYS.run_gs(write_path)

    os.remove(write_path)

### future changes ####################################
#the trn gx does not take an output folder parameter, it just puts trn files into the project folder. make the script use os to move the folders to an output folder
# have the script delete output file paths if they already exist, because I don't think the geosoft script will overwrite old files
