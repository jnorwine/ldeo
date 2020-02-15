import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import stats
import sys
import os
from tqdm import tqdm
import time
import math
pi = math.pi

### CONFIG ##############################################################

folder = "G:\\jnorwine\\polygrid1\\spc\\processed\\csv\\comparison\\" # input folder of csv files
qc_mode = 0 # set to 1 to have option to edit picks
save_plots = True
plot_path = "G:\\jnorwine\\polygrid1\\spc\\processed\\png\\comparison" # folder where plots will be saved
start_file = "row9_box0_trn.csv" # set to "" to do the whole folder

#########################################################################

def selective_regr(low_high):

    low = low_high[0]
    high = low_high[1]

    slope, intercept, r_value, p_value, std_err = stats.linregress(df["CYC/K_unit"][low:high+1], df["Ln_P"][low:high+1])

    # start point
    start_x = df["CYC/K_unit"][low]
    end_x = df["CYC/K_unit"][high]

    return start_x, end_x, slope, intercept, r_value, p_value, std_err

def on_key(event):

    global interval_list
    global edit
    global x_array
    global y_array
    global slope_list
    global edit_side
    global max_x

    start_point1 = interval_list[0][0]
    end_point1 = interval_list[0][1]
    start_point2 = interval_list[1][0]
    end_point2 = interval_list[1][1]

    if event.key == " ":
        print("spacebar")
        edit += 1
        if edit == 3:
            edit = 0

    elif event.key == "a":
        edit_side = "l"

    elif event.key == "d":
        edit_side = "r"

    elif edit == 0:

        if event.key == "left":
            int1 = (start_point1, end_point1 - 1)
            int2 = (start_point2 - 1, end_point2)
            interval_list = [int1, int2]

        elif event.key == "right":
            int1 = (start_point1, end_point1 + 1)
            int2 = (start_point2 + 1, end_point2)
            interval_list = [int1, int2]

    elif edit == 1:

        if edit_side == "r":

            if event.key == "left":

                if not end_point1 == 0:
                    int1 = (start_point1, end_point1 - 1)
                    int2 = (start_point2, end_point2)
                    interval_list = [int1, int2]

            elif event.key == "right":

                if not end_point1 == max_x:
                    int1 = (start_point1, end_point1 + 1)
                    int2 = (start_point2, end_point2)
                    interval_list = [int1, int2]

        if edit_side == "l":

            if event.key == "left":

                if not start_point1 == 0:
                    int1 = (start_point1 - 1, end_point1)
                    int2 = (start_point2, end_point2)
                    interval_list = [int1, int2]

            elif event.key == "right":

                if not start_point1 == max_x:
                    int1 = (start_point1 + 1, end_point1)
                    int2 = (start_point2, end_point2)
                    interval_list = [int1, int2]

    elif edit == 2:

        if edit_side == "r":

            if event.key == "left":

                if not end_point2 == 0:
                    int1 = (start_point1, end_point1)
                    int2 = (start_point2, end_point2 - 1)
                    interval_list = [int1, int2]

            elif event.key == "right":

                if not end_point2 == max_x:
                    int1 = (start_point1, end_point1)
                    int2 = (start_point2, end_point2 + 1)
                    interval_list = [int1, int2]

        if edit_side == "l":

            if event.key == "left":

                if not start_point2 == 0:
                    int1 = (start_point1, end_point1)
                    int2 = (start_point2 - 1, end_point2)
                    interval_list = [int1, int2]

            elif event.key == "right":

                if not start_point2 == max_x:
                    int1 = (start_point1, end_point1)
                    int2 = (start_point2 + 1, end_point2)
                    interval_list = [int1, int2]

    slope_list = []
    x_array = []
    y_array = []
    for intervals in interval_list:
        start_x, end_x, slope, intercept, r_value, p_value, std_err = selective_regr(intervals)
        start_y = slope * start_x + intercept
        end_y = slope * end_x + intercept

        xlist = [start_x, end_x]
        ylist = [start_y, end_y]
        print("slope in on_key loop: " + str(slope))
        slope_list.append(slope)

    print("edit " + str(edit))


def onpick(event):
    artist = event.artist
    ind = event.ind
    print("pick event")
    print(artist)

def animate(i):

    plt.clf()

    global interval_list
    global df
    global title
    global slope_list
    global edit_side
    global edit

    freq = df["CYC/K_unit"]
    ln_p = df["Ln_P"]

    color_tracker = ["green"] * len(interval_list)
    color_tracker[edit-1] = "red"
    if edit == 0:
        color_tracker = ["red"] * len(interval_list)

    plt.title(file)
    plt.scatter(freq, ln_p, picker=True, alpha=0.5)

    for_count = 0

    for intervals in interval_list:
        start_x, end_x, slope, intercept, r_value, p_value, std_err = selective_regr(intervals)
        start_y = slope * start_x + intercept
        end_y = slope * end_x + intercept

        xlist = [start_x, end_x]
        ylist = [start_y, end_y]
        plt.plot(xlist, ylist, c=color_tracker[for_count])

        if color_tracker[for_count] == "red":

            if edit_side == "l":
                plt.scatter(start_x, start_y, c="r", marker="x")
            elif edit_side == "r":
                plt.scatter(end_x, end_y, c="r", marker="x")

        for_count += 1

### MAIN ################################################################

def main():

    global df
    global file
    global interval_list
    global edit
    global slope_list
    global edit_side
    global max_x

    timestring = str(time.time())

    file_list = next(os.walk(folder))[2]
    if start_file != "":
        start = file_list.index(start_file)
        file_list = file_list[start:]

    slope_array = []
    name_array = []
    edit = 0 # default regr editing mode
    edit_side = "l" # default

    for file in file_list:

        df = pd.read_csv(os.path.join(folder, file))

        max_x = len(df["CYC/K_unit"]) - 1
        result_list = []

        for i in range(len(df["CYC/K_unit"])):
            interval_list = [(0, i), (i, max_x)]
            tot_r2 = 0
            r2list = []

            for interval in interval_list: # runs twice
                start_x, end_x, slope, intercept, r_value, p_value, std_err = selective_regr(interval)
                start_y = slope * start_x + intercept
                end_y = slope * end_x + intercept

                xlist = [start_x, end_x]
                ylist = [start_y, end_y]

                tot_r2 += 1 - r_value**2  # try to minimize this
                r2list.append(1 - r_value**2)

            result_list.append([tot_r2, interval_list[0], interval_list[1], r2list[0], r2list[1]])

        show_df = pd.DataFrame(result_list)
        show_df.columns = ["tot_1-r2", "int1", "int2", "minus_r2_1", "minus_r2_2"]

        fig = plt.figure()
        plt.scatter(df["CYC/K_unit"], df["Ln_P"])

        slope_list = []

        try:
            min_index = show_df["tot_1-r2"][3:].idxmin()
            interval_list = [show_df["int1"][min_index], show_df["int2"][min_index]]
            for intervals in interval_list:
                start_x, end_x, slope, intercept, r_value, p_value, std_err = selective_regr(intervals)
                start_y = slope * start_x + intercept
                end_y = slope * end_x + intercept

                xlist = [start_x, end_x]
                ylist = [start_y, end_y]

                plt.plot(xlist, ylist)
                slope_list.append(slope)
        except:
            pass

        cid = fig.canvas.mpl_connect("key_press_event", on_key)
        fig.canvas.mpl_connect("pick_event", onpick)

        if qc_mode == 1:
            ani = animation.FuncAnimation(fig, animate, interval=100)
            plt.show()

        _input = input("keep data? [y/n] slope_list: " + str(slope_list))
        if _input == "n":
            slope_list = [9999, 9999]

        slope_array.append(slope_list)
        name_array.append(file)
        if not os.path.exists(plot_path):
            os.makedirs(plot_path)
        save_path = os.path.join(plot_path, timestring + "\\" + file)
        if not os.path.exists(os.path.join(plot_path, timestring)):
            os.makedirs(os.path.join(plot_path, timestring))

        plt.title(file)
        plt.scatter(df["CYC/K_unit"], df["Ln_P"])
        for intervals in interval_list:
            start_x, end_x, slope, intercept, r_value, p_value, std_err = selective_regr(intervals)
            start_y = slope * start_x + intercept
            end_y = slope * end_x + intercept

            xlist = [start_x, end_x]
            ylist = [start_y, end_y]
            plt.plot(xlist, ylist, c="r")
        plt.savefig(save_path + ".png")
        plt.close("all")

        depth_array = np.array(slope_array) * -0.5

        depth_df = pd.DataFrame(depth_array)
        slope_df = pd.DataFrame(slope_array)
        name_series = pd.Series(name_array)

        output = pd.concat([name_series, slope_df, depth_df], axis=1)
        output.columns = ["name", "slope_1", "slope_2", "depth_1", "depth_2"]

        save_path = os.path.join(folder, "regressed\\" + timestring + "\\")
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        save_path = os.path.join(save_path, "slope_depth.csv")

        output.to_csv(save_path, index=False)

        plt.close("all")

#main()

try:
    main()
except:
    print("\nEXCEPTION IN MAIN()\n")

    #depth_array = np.array(slope_array) * -0.5 * (2*pi)**(-1)
    depth_array = np.array(slope_array) * -0.5

    depth_df = pd.DataFrame(depth_array)
    slope_df = pd.DataFrame(slope_array)
    name_series = pd.Series(name_array)

    output = pd.concat([name_series, slope_df, depth_df], axis=1)
    output.columns = ["name", "slope_1", "slope_2", "depth_1", "depth_2"]

    save_path = os.path.join(folder, "regressed\\" + str(time.time()))
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    save_path = os.path.join(save_path, "slope_depth.csv")

    output.to_csv(save_path, index=False)

    plt.close("all")


### ISSUES ################################

# ability for user to click on points to ignore them in regression (then they go translucent or something)
# option to show previous pick pngs (from some folder) next to active pick window
# fix the issue where if you use arrow keys and cross the endpoints, the script crashes
# when the script prompts for [y/n] to save data, it should only take y or no as an answer, or ask again
# remove the option to move both lines at once or implement it more nicely
# display the controls on the picking plot
# annotate code
