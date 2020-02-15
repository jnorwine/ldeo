import geosoft.gxpy as gxpy
import geosoft.gxpy.project as gxproj
import geosoft.gxapi as gxapi
import os
from tqdm import tqdm
import re

# makes windowed grids out of all .ply files in a folder from an input grid

### CONFIG ##############################

write_path = "G:\\jnorwine\\polygrid-test\\polygrid\\scratch.gs" # path to .gs scratch file (needs to be empty or not exist yet)
in_trn_folder = "G:\\jnorwine\\polygrid1\\trn_fft\\gravity\\regrid5km\\"
output_folder = "G:\\jnorwine\\polygrid1\\spc\\gravity\\regrid5km\\"

#########################################

def write_spc_gs(in_trn_path, out_spc_path, write_path):

    gs = (
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG OPENED : Fri Jul 05 13:13:32 2019\n"
    f"/-------------------------------------------------------------------------\n"
    #CURRENT        Map,"g:\jnorwine\rosetta - copy\jonnyRIS.map"
    #CURRENT        Database,"g:\jnorwine\rosetta - copy\RosettaGrid_LevellingProcess.gdb"
    #CURRENT        Grid,"g:\jnorwine\rosetta - copy\RS_TFAnom.grd(GRD)"
    f"SETINI         FFT2RSPC.TRN=\"{in_trn_path}\"\n"
    f"SETINI         FFT2RSPC.SPC=\"{out_spc_path}\"\n"
    f"SETINI         FFT2SPCFLT.SPCFILE=\"{out_spc_path}\"\n"
    f"SETINI         FFT2SMAP.SPEC=\"{out_spc_path}\"\n"
    f"GX             fft2rspc.gx\n"
    f"/-------------------------------------------------------------------------\n"
    f"/ LOG CLOSED : Fri Jul 05 13:14:03 2019\n"
    f"/-------------------------------------------------------------------------\n"
    )

    with open(write_path, "w") as file:
        file.write(gs)

def rungx():

    proj = gxproj.Geosoft_project()
    gxapi.GXSYS.set_interactive(0)
    map_path = proj.current_map
    trn_list = next(os.walk(in_trn_folder))[2]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # filter trn_list to only include .grd files
    for path in trn_list: # for some reason this does not catch .grd.xml
        if not path.endswith(".grd"):
            trn_list.remove(path)
            #print("removed " + path)

    for path in trn_list: # for some reason this does not catch .grd.gi
        newpath = path
        if not path.endswith(".grd"):
            trn_list.remove(path)
            #print("removed " + path)

    for trn in tqdm(trn_list, ascii=True):
        try:
            trn_name = re.findall(r"(.*)\.grd", trn)[0]
        except:
            pass
        out_spc_path = os.path.join(output_folder, trn_name + ".SPC")
        in_trn_path = os.path.join(in_trn_folder, trn)
        write_spc_gs(in_trn_path, out_spc_path, write_path)
        try:
            gxapi.GXSYS.run_gs(write_path)
        except:
            print("skipping " + trn)
            pass

    os.remove(write_path)

### future changes #####################################
