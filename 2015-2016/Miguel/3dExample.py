import sys
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import matplotlib.gridspec as gridspec

fitsFileI="../examples/Filters/frame-i-004264-4-0259.fits" #m81 http://mirror.sdss3.org/fields/name?name=m81
fitsFileI2="../examples/Filters/frame-i-003804-6-0084.fits" #m66 http://mirror.sdss3.org/fields/name?name=m66
fitsFileI3='../examples/Filters/frame-i-004381-2-0120.fits' #m91 http://mirror.sdss3.org/fields/name?name=m91
fitsFileI4='../examples/Filters/frame-i-002830-6-0398.fits' #m109 http://mirror.sdss3.org/fields/name?name=m109
fitsFileI5='../examples/Filters/frame-i-003805-2-0023.fits' #m59 http://mirror.sdss3.org/fields/name?name=m59
fitsFileI6='../examples/Filters/frame-i-008112-2-0074.fits' #m33 http://mirror.sdss3.org/fields/name?name=m33
fitsFileI7='../examples/Filters/frame-i-007845-2-0104.fits' #m74 http://mirror.sdss3.org/fields/name?name=m74
fitsFileI8='../examples/Filters/frame-i-003836-4-0084.fits' #m95 http://mirror.sdss3.org/fields/name?name=m95
dataset={'i':fitsFileI,'i2':fitsFileI2,'i3':fitsFileI3,'i4':fitsFileI4,'i5':fitsFileI5,'i6':fitsFileI6,'i7':fitsFileI7,'i8':fitsFileI8}

hdu_list = fits.open(dataset[sys.argv[1]])

data, header = fits.getdata(fitsFileI, header=True)
imageRaster = hdu_list[0].data

fig=plt.figure()
gs=gridspec.GridSpec(2,2)
ax = plt.subplot(gs[0,0])
ax.imshow(imageRaster, cmap='spectral', norm=LogNorm(), origin='lower')
X = np.arange(2048,step=4)
Y = np.arange(1489,step=4)
x,y = np.meshgrid(X,Y)
z=np.log(np.array([data[a,b] for b,a in zip(np.ravel(x),np.ravel(y))]))
aux=z<=0
z[aux]=0
Z=z.reshape(x.shape)

ax3=plt.subplot(gs[1,0])
plt.plot(z,'ok', ms=0.5)
plt.plot(z[0:5])
ax3=plt.subplot(gs[0:,1],projection='3d')
ax3.plot_surface(x,y,Z)
plt.show()
