import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import scipy.signal as signal
import re
from tqdm import tqdm

# plot_power_spec
# inputs: database (string), line (string), channel (string), gdb (Geosoft_gdb object), save_path (string)
# returns: dataframe
#
# creates a dataframe for the power spectrum of some line and saves a csv and plot

def csv_plot_power_spec(csv_file_path, csv_filename, save_path, spectrum_metric, lim):

    # prepare the dataframe
    df = pd.read_csv(csv_file_path + csv_filename)
    df = df.set_index(df.iloc[:, 0], drop=True)

    if spectrum_metric == "wavenumber":
        spec_met = df.index * spectrum_multiplier
    elif spectrum_metric == "wavelength":
        spec_met = df.index**(-1) * spectrum_multiplier

    # plot spectrum and save
    title = csv_file_path + csv_filename + " from csv"
    plt.figure(figsize=(12.8,9.6))
    plt.title(title)
    plt.xlabel(spectrum_metric + " (" + spectrum_unit + ")")
    plt.ylabel("ln(power)")
    plt.plot(spec_met, df.value_list, "g", label="power")
    plt.plot(spec_met, df.rolling_mean, c="m", label="rolling mean")
    upperlim = np.percentile(spec_met, 99)
    plt.xlim(left=1000, right=30000)
    plt.savefig(save_path + "png\\" + re.search(r"(.*)\.csv", csv_filename).group(1) + "_" + spectrum_metric + ".png")
    #plt.show()
    plt.close()

    return df


# close any open plots to conserve memory
plt.close("all")

##### CONFIG #################################

#spectrum_metric = "wavenumber"
spectrum_metric = "wavelength"
spectrum_unit = "m"
interval = 65 #interval between data points in the same unit as spectrum_unit
spectrum_multiplier = 65 #multiplies the x-axis, e.g. distance/fid ratio

csv_file_path = "D:\\Geosoft Projects\\Empty\\ctam_admap_2a\\csv\\"
save_path = "D:\\Geosoft Projects\\Empty\\ctam_admap_2a\\"

aggregate_filename = "bigfig-spaghetti-CTAM-ADMAP_with_ties" + " " + spectrum_metric
aggregate_title = "Rolling Mean (n=100) of Spectra for All CTAM-ADMAP Lines and Ties" + " (" + spectrum_metric + ")"

scatter_filename = "bigfig-ctam-admap_with_ties" + " " + spectrum_metric
scatter_title = "Filtered Local Maxima for All CTAM-ADMAP Lines and Ties" + " (" + spectrum_metric + ")"

tie_char = "JONNY-NORWINE" # distinct character at the beginning of line name that denotes tie lines, make it some ridiculous string if you don't want this feature

###############################################

# create list of csv files to open
csv_file_list = next(os.walk(csv_file_path))[2]

# calculate Nyquist frequency and wavelength
sample_frequency = 1 / interval
nyq_frequency = spectrum_multiplier * sample_frequency / 2
nyq_wavelength = spectrum_multiplier * 2 / sample_frequency

#set nyquist argument for csv_plot_power_spec
if spectrum_metric == "wavenumber":
    nyquist = nyq_frequency
elif spectrum_metric == "wavelength":
    nyquist = nyq_wavelength

# initialize list of dataframes
dflist = []

# set up spaghetti figure
plt.figure(figsize=(12.8,9.6))
plt.title(aggregate_title)
plt.xlabel(spectrum_metric)
plt.ylabel("ln(power)")
if spectrum_metric == "wavenumber":
    plt.ylim([-20,40])
    plt.xlim([-0.004,0.14])
elif spectrum_metric == "wavelength":
    plt.xlim([1000, 30000])
    #plt.ylim([-10, 30]) #optional, emulates RIS data limits

# set up color spectrum
color_idx = np.linspace(0, 1, len(csv_file_list))

# populate list of dataframes
for i, csv_filename in tqdm(zip(color_idx, csv_file_list), ascii=True):

    #print("working on " + csv_filename)
    df = csv_plot_power_spec(csv_file_path, csv_filename, save_path, spectrum_metric, nyquist)

    # set x-axis to be either wavenumber or wavelength
    if spectrum_metric == "wavenumber":
        spec_met = df.index * spectrum_multiplier
    elif spectrum_metric == "wavelength":
        spec_met = df.index**(-1) * spectrum_multiplier

    # plot df if it is a dataframe
    if isinstance(df, pd.DataFrame):
        dflist.append(df)
        if re.match(r"(" + re.escape(tie_char) + ")" + ".*\.csv", csv_filename):
            plt.plot(spec_met, df.rolling_mean, color=plt.cm.autumn(i))
        else:
            plt.plot(spec_met, df.rolling_mean, color=plt.cm.cool(i))


plt.savefig(save_path + aggregate_filename + ".png")

# plot and save scatter figure
plt.figure(figsize=(12.8,9.6))
plt.title(scatter_title)
plt.xlabel(spectrum_metric + " (" + spectrum_unit + ")")
plt.ylabel("ln(power)")
for df in dflist:

    plt.scatter(df.index, df.filtered_max)

#plt.savefig(save_path + scatter_filename + ".png")
#plt.show()

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
