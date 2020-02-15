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
mat_path = "G:\\jnorwine\\radar\\sir\\fft\\stack04\\lines\\decimated\\mat\\decimated\\mat\\RS01_L190_20151202_003947_level1a_SIR_69.mat"
filename = "" # output

c = 2.997924580003452e+08 # speed of light in vacuum
n_i= 1.78 # speed of light through ice
z0 = 600

###############################################################################

### PROCESS DATA ##############################################################

mat = scipy.io.loadmat(mat_path)
data = 10*np.log10(np.abs(np.real(mat["Data"])))
Time = mat["Time"].flatten()
latitude = mat["Latitude"][0]
longitude = mat["Longitude"][0]

inProj = Proj("+init=epsg:4326", preserve_flags=True) # Proj doesn't work in IPython
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

plt.figure(figsize=(20,10))
plt.imshow(data, aspect="auto", vmin=-vm, vmax=vm, cmap="seismic")
#plt.show()

###############################################################################

### SET UP BINARY HEADER ######################################################

spec = segyio.spec()

spec.sorting = 2 # sort by xlines
spec.format = 1 # IBM float format
spec.samples = range(len(data.T[0])) # number of samples per trace
spec.ilines = [0] # only one inline, right?
spec.xlines = range(len(data[0])) # one xline for every trace ?

###############################################################################

### CREATE SEGY ###############################################################

round_order = 3 # number of decimal places to which data will be rounded

with segyio.create(filename, spec) as f:
    tr = 0
    for iline in spec.ilines:
        for xline in tqdm(spec.xlines, ascii=True):

            # print("X[tr]")
            # print(X[tr])
            # print("Y[tr]")
            # print(Y[tr])
            # input()
            cdpx = int( round(X[tr], round_order) *10**round_order) # raw data too big for segy
            cdpy = int( round(Y[tr], round_order) *10**round_order) #
            ns = len(data.T[0])

            scalco = -1*int(10**round_order)

            f.header[tr] = {segyio.su.offset : 0,
                            segyio.su.cdp : tr+1,
                            segyio.su.tracr : tr+1, # TRACE_SEQUENCE_FILE
                            segyio.su.xline : tr+1,
                            segyio.su.counit : 1,
                            segyio.su.iline : iline,
                            segyio.su.xline : xline,
                            segyio.su.dt : dt, # TRACE_SAMPLE_INTERVAL
                            segyio.su.scalco : scalco, # SourceGroupScalar
                            segyio.su.gx : cdpx,
                            segyio.su.gy : cdpy,
                            segyio.su.cdpx : cdpx,
                            segyio.su.cdpy : cdpy,
                            segyio.su.ns : ns} # TRACE_SAMPLE_COUNT

            f.trace[tr] = np.float32(data.T)[tr]
            tr += 1

print("Done.")

###############################################################################

### ISSUES ####################################################################
