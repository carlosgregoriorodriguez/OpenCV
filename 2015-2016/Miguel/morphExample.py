from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cv2
import sys
import numpy as np


fitsFileI="../TFG/frame-i-004264-4-0259.fits" #m81 http://mirror.sdss3.org/fields/name?name=m81
fitsFileI2="../TFG/frame-i-003804-6-0084.fits" #m66 http://mirror.sdss3.org/fields/name?name=m66
fitsFileI3='../TFG/frame-i-004381-2-0120.fits' #m91 http://mirror.sdss3.org/fields/name?name=m91
fitsFileI4='../TFG/frame-i-002830-6-0398.fits' #m109 http://mirror.sdss3.org/fields/name?name=m109
fitsFileI5='../TFG/frame-i-003805-2-0023.fits' #m59 http://mirror.sdss3.org/fields/name?name=m59
fitsFileI6='../TFG/frame-i-008112-2-0074.fits' #m33 http://mirror.sdss3.org/fields/name?name=m33
fitsFileI7='../TFG/frame-i-007845-2-0104.fits' #m74 http://mirror.sdss3.org/fields/name?name=m74
fitsFileI8='../TFG/frame-i-003836-4-0084.fits' #m95 http://mirror.sdss3.org/fields/name?name=m95
data= fits.getdata(fitsFileI)
hdu_list = fits.open(fitsFileI)
img = hdu_list[0].data
Min=np.amin(img)
Max=np.amax(img)
img = 255*(img+abs(Min))/Max
imgFiltered=cv2.filter2D(img,-1,np.array([[0,1,0],[1,0,1],[0,1,0]]))
_,imgBase=cv2.threshold(imgFiltered, cv2.THRESH_OTSU, 0, cv2.THRESH_TOZERO_INV)
cv2.namedWindow('Base image', cv2.WINDOW_NORMAL)
cv2.imshow('Base image', imgBase)


def nada(o):
	print "Operation used:", Operations[o]
def nada2(i):
	print "Number of iterations:", i
cv2.namedWindow('img processed', cv2.WINDOW_NORMAL)
cv2.createTrackbar('operation', 'img processed', 0, 4, nada)
operations=[cv2.MORPH_OPEN,cv2.MORPH_CLOSE,cv2.MORPH_GRADIENT,cv2.MORPH_TOPHAT,cv2.MORPH_BLACKHAT]
Operations=['Open', 'Close', 'Gradient', 'Top hat','Black hat', 'Hit and miss']
nada2(1)
cv2.createTrackbar('iterations', 'img processed', 0, 50, nada2)
while True:
	operation=cv2.getTrackbarPos('operation', 'img processed')
	number_of_iterations=cv2.getTrackbarPos('iterations', 'img processed')
	imgProcessed=cv2.morphologyEx(imgBase, operations[operation], (3,3),iterations=number_of_iterations)
	cv2.imshow('img processed',imgProcessed)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break
cv2.destroyAllWindows()
