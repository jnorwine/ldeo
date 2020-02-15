import segyio
import numpy as np
import pandas as pd
import scipy.io
import scipy.interpolate
import matplotlib.pyplot as plt
from tqdm import tqdm
import math
from pyproj import Proj, transform


### CONFIG ####################################################################

#mat = "W:\\trunk\\icepod\\antarctica\\20152016\\radar\\sir\\fft\\stack04\\lines\\L190\\decimated\\mat\\RS01_L190_20151202_004447_level1a_SIR_70.mat"
mat_path = "G:\\jnorwine\\radar\\sir\\fft\\stack04\\lines\\decimated\\mat\\decimated\\mat\\RS01_L190_20151202_005447_level1a_SIR_72.mat"
filename = "G:\\jnorwine\\Python SegY\\test2-iline0.sgy"

c = 2.997924580003452e+08 # speed of light in vacuum
n_i= 1.78 # speed of light through ice
z0 = 600

###############################################################################

### PROCESS DATA ##############################################################

print("loading .mat...")
mat = scipy.io.loadmat(mat_path)
data = 10*np.log10(np.abs(np.real(mat["Data"])))
Time = mat["Time"].flatten()
latitude = mat["Latitude"][0]
longitude = mat["Longitude"][0]

inProj = Proj("+init=epsg:4326", preserve_flags=True) # doesn't work in IPython
outProj = Proj("+init=epsg:3031", preserve_flags=True)

X = []
Y = []
for i in range(len(latitude)):
    x, y = transform(inProj, outProj, longitude[i], latitude[i])
    X.append(x)
    Y.append(y)

Dist = np.insert(np.cumsum(np.hypot(np.diff(X), np.diff(Y))), 0, 0)

Time = Time[Time >= 0]
Data = data[Time >= 0][:]

# Time is in microseconds, so dt is less than 1 microsecond. Convert it to picoseconds to make it fit in an integer
dt = (Time[1] - Time[0])*1e6 # this is how it was in JK's script, but it's still < 0 and needs to be an integer for trace header
dt = dt * 1e6 # converts to picoseconds
dt = int(dt) # converts to integer

###############################################################################

### DATA PREVIEW ##############################################################

vm = np.percentile(data, 99)

print("plotting...")
plt.figure(figsize=(20,10))
plt.imshow(data, aspect="auto", vmin=-vm, vmax=vm, cmap="gray")
plt.show()

###############################################################################

### ISSUES ####################################################################
