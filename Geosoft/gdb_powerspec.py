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

def rungx():

    # close any open plots to conserve memory
    plt.close("all")

    # messages and inputs to user
    gxapi.GXSYS.display_message("Reminder", "You need to save the database and select any cell in the spectrum channel.")

    ######################################################
    #save_path = gxproj.get_user_input(title="Path", prompt="Path (should end with backslash and all backslashes must be doubled \\\\)", kind="string")
    save_path = "D:\\Geosoft Projects\\Spectra\\power_spectra\\VL-ADMAP\\"
    ######################################################

    # get and store information about the geosoft project
    proj = gxproj.Geosoft_project()
    db_state = proj.current_db_state()
    database = proj.current_database
    channel = db_state["selection"][1]
    line = db_state["selection"][0]
    gdb = gxdb.Geosoft_gdb.open(database)
    line_list = gdb.lines().keys()

    # initialize list of dataframes
    dflist = []

    ### set up aggregate figure ##########################
    aggregate_filename = "bigfig-spaghetti-VL-ADMAP"
    aggregate_title = "Rolling Mean (n=100) of Spectra for All VL-ADMAP Lines and Ties"
    ######################################################

    plt.figure(figsize=(12.8,9.6))
    plt.title(aggregate_title)
    plt.xlabel("wavelength")
    plt.ylabel("power")
    plt.ylim([-20,40])
    #plt.xlim([0,0.015])

    # populate list of dataframes
    for line in tqdm(line_list, ascii=True):

        #print("working on " + line)
        df = plot_power_spec(database, line, channel, gdb, save_path)

        if isinstance(df, pd.DataFrame):
            dflist.append(df)
            plt.plot(df.index**(-1), df.rolling_mean)

    plt.savefig(save_path + aggregate_filename + ".png")
    plt.show()

    ### set figure parameters #############################
    scatter_filename = "bigfig-vl-admap"
    scatter_title = "Filtered Local Maxima for VL-ADMAP Lines and Ties"
    #######################################################

    # plot, show, and save figure
    plt.figure(figsize=(12.8,9.6))
    plt.title(scatter_title)
    plt.xlabel("wavelength")
    plt.ylabel("power")
    for df in dflist:

        plt.scatter(df.index**(-1), df.filtered_max)

    plt.savefig(save_path + scatter_filename + ".png")
    plt.show()


# plot_power_spec
# inputs: database (string), line (string), channel (string), gdb (Geosoft_gdb object), save_path (string)
# returns: dataframe
#
# creates a dataframe for the power spectrum of some line and saves a csv and plot

def plot_power_spec(database, line, channel, gdb, save_path):

    # parse information about the line and channel
    channel_array = gdb.read_channel(line, channel)
    value_list = channel_array[0]
    fid_start = channel_array[1][0]
    fid_incr = channel_array[1][1]

    if value_list.sum() == 0:
        print(line + " is empty, skipping")
        return "empty"

    # initialize list of fiducials
    fid_list = []

    # populate list of fiducials
    for i in range(len(value_list)):
        fid_list.append(fid_start + fid_incr * i)

    # create a series from value_list
    vl = pd.Series(value_list)

    # create a dataframe indexed by fid_list containing value_list
    df = pd.DataFrame(value_list, index=fid_list, columns=["value_list"])

    # calculate rolling mean, max, and rolling mean of max and add to dataframe
    df["rolling_mean"] = df.rolling(window=100).mean()
    df["rolling_max"] = vl.rolling(window=100).max().values
    df["rolling_mean_max"] = df["rolling_max"].rolling(window=7000).mean().values

    # find relative extrema and filter them
    n = 1500 # number of points to be checked before and after by argrelextrema
    df["max"] = df.iloc[signal.argrelextrema(df.value_list.values, np.greater_equal, order=n)[0]]["value_list"]
    df["rolling_max2"] = df.rolling_max.values**2
    df["rolling_mean_max2"] = df["rolling_max2"].rolling(window=1500).mean().values
    df["filtered_max"] = df["max"][df["max"]**2 > df.rolling_mean_max2 + 0.1 * df.rolling_max2.std()]

    # save csv of dataframe
    df.to_csv(save_path + "csv\\" + line + ".csv")

    # plot spectrum and save
    title = database + " line " + line + " relmax order " + str(n) + " 99th percentile"
    plt.figure(figsize=(12.8,9.6))
    plt.title(title)
    plt.xlabel("wavelength")
    plt.ylabel(channel)
    upperlim = np.percentile(df.index**(-1), 99)
    plt.xlim([0, upperlim])
    plt.plot(df.index**(-1), value_list, "g", label="power")
    #plt.scatter(fid_list, df["max"], c="m", label="relative maximum")
    plt.savefig(save_path + "png\\" + line + ".png" )
    #plt.show()
    plt.close()

    return df

# output from current_db_state()
# {'disp_chan_list': ['test_channel'], 'selection': ('L0', 'test_channel', '6', '6')}

# FEATURES TO BUILD
# use regex to pull just the *.db for the title instead of the full path
# use current_db_state to allow user to plot either the entire line or just selected fids
# make save path an optional argument of plot_power_spec()

# TEST AREA
#df = pd.read_csv("D:\\Geosoft Projects\\Empty\\power_spectra\\csv\\L190.csv")
#df["rolling_max2"] = df.rolling_max ** 2
#df["rolling_mean_max2"] = df["rolling_max2"].rolling(window=1500).mean().values
#plt.plot(df.rolling_max2[2500:])
#plt.plot(df.rolling_mean_max2 + 0.1 * df.rolling_max2.std())
#plt.plot(3 * df.rolling_max.diff() / df.index.to_series().diff())
