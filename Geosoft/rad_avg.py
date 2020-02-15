import numpy as np
import geosoft.gxpy as gxpy
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
import pandas as pd

#grid_path = "G:\\jnorwine\\polygrid1\\trn_fft\\gravity\\regrid5km\\row6_box8_trn_output.grd"
grid_path = "G:\\jnorwine\\polygrid1\\trn_fft\\gravity\\row6_box8_trn_output.grd"
bins = 50

# From Bi Rico on StackOverflow
def radial_profile(data, center):
    y, x = np.indices((data.shape))

# running as stand-alone program
if __name__ == "__main__":

    # Stand-alone programs must create a GX context before calling Geosoft methods.
    with gxpy.gx.GXpy() as gxc:

        with gxpy.grid.Grid.open(grid_path) as grid:

            f = grid.np()
            sx, sy = f.shape
            X, Y = np.ogrid[0:sx, 0:sy]

            r = np.hypot(X - sx/2, Y) # r is the same shape as grid, contains radius to every point

            print(pd.DataFrame((bins * (r/r.max())).astype(np.int)))

            # you need to correlate the bin numbers with their radii (frequency in CYC/km)

            rbin = (bins* r/r.max()).astype(np.int) # array where each position has its bin number
            index=np.arange(1, rbin.max() +1) # array from 1 to rbin.max()
            radial_mean = ndimage.mean(f, labels=rbin, index=index)

            plt.figure()
            plt.title("with rbins")
            plt.scatter(index, radial_mean)
            plt.show()
