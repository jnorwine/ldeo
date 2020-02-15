import geosoft.gxpy as gxpy
import geosoft.gxpy.gdb as gxdb
import geosoft.gxpy.project as gxproj
import numpy as np
import os
import datetime



def rungx():

    line = gxproj.get_user_input(title="test", prompt="line?", kind="string")
    rownumber = gxproj.get_user_input(title="test", prompt="Row Number", kind="string")

    channel_list = ["UTCTime2", "unixtime", "Latitude", "Longitude", "SurfHell_lidar"]
    new_row_list = []
    list_of_rows = []


    # gxpy.utility.display_message("GX Python", np.version.version)

    gdb = gxdb.Geosoft_gdb.open()



    for channel in channel_list:
        print("testing on row " + str(rownumber))

        if channel == "UTCTime2":
            print(str(datetime.timedelta(seconds = gdb.read_channel(line, channel)[0][1] * 60**2)))
            new_row_list.append(str(datetime.timedelta(seconds = gdb.read_channel(line, channel)[0][1] * 60**2)))

        else:
            print(gdb.read_channel(line, channel)[0][1])
            new_row_list.append(gdb.read_channel(line, channel)[0][1])

        input("done with channel")

    print(new_row_list)
    list_of_rows.append(new_row_list)

    input("done with row")
