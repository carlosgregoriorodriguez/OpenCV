from astropy.io import fits

fitsFile="../examples/Filters/frame-i-002830-6-0398.fits"
data, header = fits.getdata(fitsFile, header=True)
print "HEADER:\n", header
print "DATA:\n", data
hdu_list = fits.open(fitsFile)
hdu_list.info()
