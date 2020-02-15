import geosoft.gxpy as gxpy
import geosoft.gxpy.gdb as gxdb
import geosoft.gxpy.project as gxproj
import geosoft.gxapi as gxapi
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.signal as signal


def rungx():

    proj = gxproj.Geosoft_project()
    db_state = proj.current_db_state()

    gxapi.GXSYS.display_message("Caution", "This plot will show the most recent SAVED version of the database!")
    #database = gxproj.get_user_input(title="Database", prompt="Enter database name:", kind="string")
    database = proj.current_database
    channel = db_state["selection"][1]
    line = db_state["selection"][0]


    channel_list = [] # future version could allow for multiple channels
    fid_list = []

    # gxpy.utility.display_message("GX Python", np.version.version)

    gdb = gxdb.Geosoft_gdb.open(database)

    channel_array = gdb.read_channel(line, channel)
    value_list = channel_array[0]
    fid_start = channel_array[1][0]
    fid_incr = channel_array[1][1]

    analytic_signal = signal.hilbert(np.array(value_list))
    amplitude_envelope = np.abs(analytic_signal)



    for i in range(len(value_list)):
        fid_list.append(fid_start + fid_incr * i)


    plt.title(database + " line " + line)
    plt.xlabel("Fid")
    plt.ylabel(channel)
    plt.plot(fid_list, value_list, "g", label="power")
    plt.plot(fid_list, amplitude_envelope, "r", label="envelope")
    plt.legend()
    #plt.show()


# output from current_db_state()
# {'disp_chan_list': ['test_channel'], 'selection': ('L0', 'test_channel', '6', '6')}

# FEATURES TO BUILD
# use regex to pull just the *.db for the title instead of the full path
# use current_db_state to allow user to plot either the entire line or just selected fids
# remove power spectra specific features
