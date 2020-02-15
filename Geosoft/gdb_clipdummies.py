import geosoft.gxpy as gxpy
import geosoft.gxpy.gdb as gxdb
import geosoft.gxpy.project as gxproj
import geosoft.gxapi as gxapi
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import scipy.signal as signal
from tqdm import tqdm

def line_to_df(gdb, line, filter_channel):

    line_array = gdb.read_line(line)
    label_list = line_array[1]
    fid_tuple = line_array[2]

    fid_list = []
    for i in range(line_array[0].shape[0]):
        fid_list.append(fid_tuple[0] + fid_tuple[1] * i)

    df = pd.DataFrame(line_array[0])
    df.columns = line_array[1]
    df.index = fid_list

    return df, fid_tuple

def df_to_gdb(df, gdb_name, line_name, fid_tuple):

    try:
        new_gdb = gxdb.Geosoft_gdb.new(gdb_name, 10000, 500)

    except:
        new_gdb = gxdb.Geosoft_gdb.open(gdb_name)

    for column in df:
        new_gdb.new_channel(column) # skips if it already exists
        new_gdb.write_channel(line_name, column, df[column], fid_tuple)

def rungx():

    ##############################################

    # user must select in Geosoft the channel to be referenced

    ##############################################

    proj = gxproj.Geosoft_project()
    db_state = proj.current_db_state()
    database = proj.current_database
    selected_channel = db_state["selection"][1]
    line = db_state["selection"][0]
    gdb = gxdb.Geosoft_gdb.open(database)
    line_list = list(gdb.lines().keys())
    channel_list = list(gdb.list_channels().keys())

    dflist = []
    fid_tuple_list = []
    filter_channel = selected_channel

    for line in tqdm(line_list, ascii=True):
        df, fid_tuple = line_to_df(gdb, line, selected_channel)
        filtered_df = df[pd.notnull(df[filter_channel])]
        dflist.append(filtered_df)
        fid_tuple_list.append(fid_tuple)
        df_to_gdb(filtered_df, database + "_clipped", line, fid_tuple)
