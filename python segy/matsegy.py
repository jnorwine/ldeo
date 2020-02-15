#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Jonny Norwine
# Adapted from MATLAB scripts by Jonny Kingslake
# Last updated July 18, 2019


# In[3]:


import segyio
import numpy as np
import pandas as pd
import scipy.io
import scipy.interpolate
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from tqdm import tqdm
import math


# In[4]:


def RadargramElevationCorrection2(FlightElevation, PlaneHeight, Time, Data, z0):

    SurfMesh = np.repeat(2*PlaneHeight/c, Data.T.shape[0])
    zs_Mesh = np.repeat(FlightElev-PlaneHeight, Data.T.shape[0])

    TWTT_HcorrectionMesh = 2*(z0-zs_Mesh)*n_i/c

    TWTT_Hcorrection = np.array([TWTT_HcorrectionMesh])[0][:]

    Mesh = np.meshgrid(range(1, Data.T.shape[1]), Time)
    SpaceMesh = Mesh[0]
    TimeMesh = Mesh[1]

    Data3Function = scipy.interpolate.interp2d(SpaceMesh, TimeMesh, Data)
    Data3 = Data3Function(SpaceMesh, SurfMesh+TimeMesh-TWTT_HCorrectionMesh)

    return Data3, TWTT_Hcorrection


# In[5]:


def geog_to_pol_wgs84_71S(latitude, longitude):

    dtorad = math.pi / 180

    phi_c = -71
    lon0 = 0

    a = 6378137;
    f = 1/298.257223563;
    e2 = 2*f-f**2;
    e = math.sqrt(e2);

    m_c = math.cos(phi_c*dtorad)/math.sqrt(1-e2*(math.sin(phi_c*dtorad))**2)
    t_c = math.tan(math.pi/4+phi_c*dtorad/2)/ ( (1+e*math.sin(phi_c*dtorad))/(1-e*math.sin(phi_c*dtorad)) )**(e/2)

    t = []
    latnum = 0

    for lat in latitude:
        t_ = math.tan(math.pi/4+lat*dtorad/2) / ( (1+e*math.sin(lat*dtorad)) / (1-e*math.sin(lat*dtorad)) )
        t.append(t_)

    rho=[a*m_c*t_/t_c for t_ in t]

    x = []
    y = []

    lonnum = 0
    for lon in longitude:
        x_ = -rho[lonnum] * math.sin((lon0 - lon)*dtorad)
        y_ = rho[lonnum] * math.cos((lon0-lon)*dtorad)
        lonnum += 1
        x.append(x_)
        y.append(y_)

    return x, y


# In[6]:


# CONFIG

#mat = "W:\\trunk\\icepod\\antarctica\\20152016\\radar\\sir\\fft\\stack04\\lines\\L190\\decimated\\mat\\RS01_L190_20151202_004447_level1a_SIR_70.mat"
mat = "G:\\jnorwine\\radar\\sir\\fft\\stack04\\lines\\decimated\\mat\\decimated\\mat\\RS01_L190_20151202_003947_level1a_SIR_69.mat"
filename = "F:\\jnorwine\\Python SegY\\test.sgy"

c = 2.997924580003452e+08 # speed of light in vacuum
n_i= 1.78 # speed of light through ice
z0 = 600


# In[7]:


# PROCESS DATA

mat = scipy.io.loadmat(mat)
data = 10*np.log10(np.abs(np.real(mat["Data"])))
Time = mat["Time"].flatten()
latitude = mat["Latitude"][0]
longitude = mat["Longitude"][0]

X, Y = geog_to_pol_wgs84_71S(latitude, longitude)
Dist = np.insert(np.cumsum(np.hypot(np.diff(X), np.diff(Y))), 0, 0)

Time = Time[Time >= 0]
Data = data[Time >= 0][:]

dt = (Time[1]-Time[0])*1e6


# In[6]:


# ELEVATION CORRECTION

FlightElev = mat["Elevation"] + mat["Surf_Elev"]
PlaneHeight = mat["Elevation"]
Data2, SurfaceTWTTnew = RadargramElevationCorrection2(FlightElev, PlaneHeight, Time, Data, z0)


# In[ ]:


# DATA PREVIEW

vm = np.percentile(data, 99)

plt.figure(figsize=(20,10))
plt.imshow(data, aspect="auto", vmin=-vm, vmax=vm, cmap="seismic")
plt.show()


# In[ ]:


# EDITED DATA PREVIEW FOR TESTING

vm = np.percentile(data, 99)

plt.figure(figsize=(20,10))
plt.imshow(data, aspect="auto", vmin=-vm, vmax=vm, cmap="seismic")
plt.show()


# In[ ]:


# SET UP SEGY

spec = segyio.spec()

spec.sorting = 2 # sort by xlines
spec.format = 1 # IBM float format
spec.samples = range(len(data.T[0])) # number of samples per trace
spec.ilines = [1] # only one inline, right?
spec.xlines = range(len(data[0])) # one xline for every trace ?


# In[ ]:


# CREATE SEGY

with segyio.create(filename, spec) as f:
    tr = 0
    for iline in spec.ilines:
        for xline in tqdm(spec.xlines):
            f.header[tr] = {segyio.su.offset : 0,
                            segyio.su.iline : iline,
                            segyio.su.xline : xline
                            segyio.su.dt : dt
                            segyio.su.cdpx : X[tr]
                            segyio.su.cdpy : Y[tr]}
            f.trace[tr] = np.float32(data.T)[tr]
            tr += 1


# In[9]:


### TESTING ELEVATION CORRECTION

FlightElev = mat["Elevation"] + mat["Surf_Elev"]
PlaneHeight = mat["Elevation"]


SurfMesh = np.meshgrid(2*PlaneHeight/c, range(Data.T.shape[1]))[0]

zs_Mesh = np.meshgrid(FlightElev-PlaneHeight, Data.T.shape[1])[0]

TWTT_HcorrectionMesh = 2*(z0-zs_Mesh)*n_i/c
TWTT_Hcorrection = np.array([TWTT_HcorrectionMesh])[0][:]

SpaceMesh, TimeMesh = np.meshgrid(range(0, Data.T.shape[0]), Time)

spline = scipy.interpolate.RectBivariateSpline(SpaceMesh[0], TimeMesh[:,0], Data.T)
Data3 = spline(SpaceMesh, SurfMesh+TimeMesh-TWTT_HcorrectionMesh)

SpaceMesh.shape
