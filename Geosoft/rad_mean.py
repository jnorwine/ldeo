# CODE FROM SCIPY-LECTURES.ORG
# http://scipy-lectures.org/advanced/image_processing/auto_examples/plot_radial_mean.html

import numpy as np
import scipy
from scipy import ndimage
import matplotlib.pyplot as plt

bins = 50


f = ndimage.imread("C:\\Users\\Jonny\\Desktop\\testspec.png", flatten=True)
#f = scipy.misc.face(gray=True)
sx, sy = f.shape
X, Y = np.ogrid[0:sx, 0:sy]

r = np.hypot(X - sx/2, Y)

rbin = (bins* r/r.max()).astype(np.int)
radial_mean = ndimage.mean(f, labels=rbin, index=np.arange(1, rbin.max() +1))

plt.figure(figsize=(5, 5))
plt.axes([0, 0, 1, 1])
plt.imshow(rbin, cmap="gray")
plt.axis('off')

plt.show()
