import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import sys

### CONFIG ####################################################################

xy_pair = ("CYC/K_unit", "Ln_P")

###############################################################################

def prompt_user(lims):

    if lims != []:
        print("optional arguments --samex, --samey")
    user_input = input("file path: ")
    path = re.findall(r"^(.+\.csv)", user_input)[0]
    title = re.findall(r"\\([^\\]+)\.csv", path)[0]
    try:
        argstring = re.findall(r"^(?:.+\.csv)(.+)", user_input)[0]
        arglist = re.findall(r"--[^\s]+", argstring)
    except:
        arglist = []

    df = pd.read_csv(path)
    fig = plt.figure()
    plt.ion()
    plt.title(title)
    plt.xlabel(xy_pair[0])
    plt.ylabel(xy_pair[1])
    plt.plot(df[xy_pair[0]], df[xy_pair[1]])

    if "--samex" in arglist:
        plt.xlim(lims[0])

    if "--samey" in arglist:
        plt.ylim(lims[1])

    if "--depth" in arglist:
        x = df[xy_pair[0]]
        y = df[xy_pair[2]]
        dydx = np.diff(y) / np.diff(x)
        depth = (-1/2) * dydx
        plt.plot(x, depth)

    axes = fig.axes[0]
    xlim = axes.get_xlim()
    ylim = axes.get_ylim()
    lims = [xlim, ylim]

    plt.show()

    answer = input("\nexit or plot?\n")
    return (answer, lims)

### MAIN #######################################################################

lims = []
response = prompt_user(lims)
answer = response[0]
lims = response[1]

while answer != "exit":
    response = prompt_user(lims)
    answer = response[0]
    lims = response[1]

plt.close("all")
