from astropy.io import fits
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import os




fitsFileI="frame-i-004264-4-0259.fits"#"frame-i-006073-4-0063.fits"#"HorseHead.fits"
fitsFileU="frame-u-004264-4-0259.fits"#"frame-i-006073-4-0063.fits"#"HorseHead.fits"
fitsFileR="frame-r-004264-4-0259.fits"#"frame-i-006073-4-0063.fits"#"HorseHead.fits"
fitsFileG="frame-g-004264-4-0259.fits"#"frame-i-006073-4-0063.fits"#"HorseHead.fits"
data, header = fits.getdata(fitsFileI, header=True)
print header
#print data
print "*****************"
##RdYlGn

hdu_list = fits.open(fitsFileI)
hdu_list.info()
fig = plt.figure()
ax = fig.add_subplot(2,2,1)
imageRaster = hdu_list[0].data
ax.imshow(imageRaster, cmap='spectral', norm=LogNorm(), origin='lower')

hdu_list = fits.open(fitsFileU)
hdu_list.info()
ax2 = fig.add_subplot(2,2,2, sharex = ax, sharey = ax )
imageRaster = hdu_list[0].data
ax2.imshow(imageRaster, cmap='spectral', norm=LogNorm(), origin='lower')

hdu_list = fits.open(fitsFileR)
hdu_list.info()
ax3 = fig.add_subplot(2,2,3, sharex = ax, sharey = ax )
imageRaster = hdu_list[0].data
ax3.imshow(imageRaster, cmap='spectral', norm=LogNorm(), origin='lower')


hdu_list = fits.open(fitsFileG)
hdu_list.info()
ax4 = fig.add_subplot(2,2,4, sharex = ax, sharey = ax )
imageRaster = hdu_list[0].data
ax4.imshow(imageRaster, cmap='spectral', norm=LogNorm(), origin='lower')

plt.show()
print "Pintado OK"



#print(type(imageRaster.flat))
#NBINS = 1000
#histogram = plt.hist(imageRaster.flat, NBINS)
#plt.show()
hdu_list.close()
'''
if os.path.isfile(fitsFile): print "OK path"

imgRaster = fits.getdata(fitsFile)
image_data = hdu_list[0].data
print(type(imgRaster))
print('Min:', np.min(imgRaster),'Max:', np.max(imgRaster))
print imgRaster.shape
plt.imshow(imgRaster, cmap='gray')
plt.colorbar()

'''

'''
hdu_number = 0
fits.getheader('input_file.fits', hdu_number)

print(type(data))
print(header["NAXIS"])
'''
