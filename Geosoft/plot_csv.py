import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import sys

### CONFIG ####################################################################

xy_pair = ("CYC/K_unit", "Ln_P", "5_DEPTH")

###############################################################################

def prompt_user(limlist):

    if limlist == []:
	    print("optional argument --depth")
    else:
        print("optional arguments --samex, --samey, --depth")
    user_input = input("file path: ")
    path = re.findall(r"^(.+\.csv)", user_input)[0]
    title = re.findall(r"\\([^\\]+)\.csv", path)[0]
    try:
        argstring = re.findall(r"^(?:.+\.csv)(.+)", user_input)[0]
        arglist = re.findall(r"--[^\s]+", argstring)
    except:
        arglist = []

    df = pd.read_csv(path)
    fig = plt.figure(title, figsize=(9, 6))
    plt.ion()
    #fig.suptitle(title)
    
    if "--depth" in arglist:
        plt.subplot(2, 1, 1)
    plt.xlabel(xy_pair[0])
    plt.ylabel(xy_pair[1])
    plt.scatter(df[xy_pair[0]], df[xy_pair[1]], c="g", s=12)
    plt.title("Frequency Spectrum")
    plt.grid()

    if "--samex" in arglist:
        plt.xlim(limlist[0][0])

    if "--samey" in arglist:
        plt.ylim(limlist[0][1])

    if "--depth" in arglist:
        plt.subplot(2, 1, 2)
        depth = df[xy_pair[2]][2:-2].astype("float64")
        plt.scatter(df[xy_pair[0]][2:-2], depth, c="r", s=12)
        #plt.xlim(xlim)
        plt.title("Mean Depth to Source")
        plt.xlabel(xy_pair[0])
        plt.ylabel("depth (K_unit)")
        plt.grid()
        if "--samex" in arglist:
            plt.xlim(limlist[1][0])

        if "--samey" in arglist:
            plt.ylim(limlist[1][1])

    axes = fig.axes
    limlist = [[axes[0].get_xlim(), axes[0].get_ylim()], [axes[1].get_xlim(), axes[1].get_ylim()]]

    fig.tight_layout()
    fig.show()

    answer = input("\nexit or plot?\n")
    return (answer, limlist)

### MAIN #######################################################################

limlist = []
response = prompt_user(limlist)
answer = response[0]
limlist = response[1]

while answer != "exit":
    response = prompt_user(limlist)
    answer = response[0]
    limlist = response[1]

plt.close("all")
