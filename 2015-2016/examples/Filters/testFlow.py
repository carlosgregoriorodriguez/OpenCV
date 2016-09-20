# -*- coding: utf-8 -*-
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cv2
import sys
import numpy as np



fitsFileI="frame-i-004264-4-0259.fits" #m81 http://mirror.sdss3.org/fields/name?name=m81
fitsFileU="frame-u-004264-4-0259.fits" #m81
fitsFileR="frame-r-004264-4-0259.fits" #m81 
fitsFileG="frame-g-004264-4-0259.fits" #m81
f1="f1.jpg"
fitsFileI2="frame-i-003804-6-0084.fits" #m66 http://mirror.sdss3.org/fields/name?name=m66
fitsFileU2="frame-u-003804-6-0084.fits" #m66
fitsFileR2="frame-r-003804-6-0084.fits" #m66
fitsFileG2="frame-g-003804-6-0084.fits" #m66
fitsFileI3='frame-i-004381-2-0120.fits' #m91 http://mirror.sdss3.org/fields/name?name=m91
fitsFileI4='frame-i-002830-6-0398.fits' #m109 http://mirror.sdss3.org/fields/name?name=m109
fitsFileI5='frame-i-003805-2-0023.fits' #m59 http://mirror.sdss3.org/fields/name?name=m59
fitsFileI6='frame-i-008112-2-0074.fits' #m33 http://mirror.sdss3.org/fields/name?name=m33
fitsFileI7='frame-i-007845-2-0104.fits' #m74 http://mirror.sdss3.org/fields/name?name=m74
fitsFileI8='frame-i-003836-4-0084.fits' #m95 http://mirror.sdss3.org/fields/name?name=m95
dataset={'i':fitsFileI,'u':fitsFileU,'r':fitsFileR,'g':fitsFileG,'1':f1,'i2':fitsFileI2,'u2':fitsFileU2,'r2':fitsFileR2,'g2':fitsFileG2,'i3':fitsFileI3,'i4':fitsFileI4,'i5':fitsFileI5,'i6':fitsFileI6,'i7':fitsFileI7,'i8':fitsFileI8}

if len(sys.argv)==2:
	data = fits.getdata(dataset[sys.argv[1]])
	#print header
	hdu_list = fits.open(dataset[sys.argv[1]])
	#hdu_list.info()
	img = hdu_list[0].data
	Min=np.amin(img)
	Max=np.amax(img)
	img = 255*(img+abs(Min))/Max
#else:
#	img=255*cv2.imread(dataset[sys.argv[1]],0)

print img.shape,type(img),np.amax(img),np.amin(img)

#cv2.namedWindow("img", cv2.WINDOW_NORMAL)
#cv2.imshow('img',img)

#plt.imshow(img,cmap='spectral', norm=LogNorm(), origin='lower')
#plt.show()


imgBlur = cv2.blur(img,(3,3))
print "BLUR: ",imgBlur.shape,type(imgBlur),np.amax(imgBlur),np.amin(imgBlur)
#cv2.namedWindow("imgBlur", cv2.WINDOW_NORMAL)
#cv2.imshow('imgBlur',imgBlur)


imgFiltered=cv2.filter2D(img,-1,np.array([[0,1,0],[1,0,1],[0,1,0]]))
print "CUSTOM FILTER: ",imgFiltered.shape,type(imgFiltered),np.amax(imgFiltered),np.amin(imgFiltered)
#cv2.namedWindow("imgFiltered", cv2.WINDOW_NORMAL)
#cv2.imshow('imgFiltered',imgFiltered)


imgGB=cv2.GaussianBlur(img,(3,3),1)
print "G. BLUR: ",imgGB.shape,type(imgGB),np.amax(imgGB),np.amin(imgGB)
#cv2.namedWindow("imgGB", cv2.WINDOW_NORMAL)
#cv2.imshow('imgGB',imgGB)


imgM=cv2.morphologyEx(img, cv2.MORPH_GRADIENT,(3,3))
print "MORPH:", imgM.shape,type(imgM),np.amax(imgM),np.amin(imgM)
#cv2.namedWindow("imgM", cv2.WINDOW_NORMAL)
#cv2.imshow('imgM',imgM)


imgL=cv2.Laplacian(img,-1)
print "LAPLACIAN:",imgL.shape,type(imgL),np.amax(imgL),np.amin(imgL)
#cv2.namedWindow("imgL", cv2.WINDOW_NORMAL)
#cv2.imshow('imgL',imgL)


imgS=cv2.Sobel(img,-1,3,2,ksize=5)
print "SOBEL:", imgS.shape,type(imgS),np.amax(imgS),np.amin(imgS)
#cv2.namedWindow("imgS", cv2.WINDOW_NORMAL)
#cv2.imshow('imgS',imgS)



imgH=cv2.cornerHarris(img,3,3,0.0005)
print "HARRIS: ",imgH.shape,type(imgH),np.amax(imgH),np.amin(imgH)





def nada3(t):
	print "Filter used as base image:", Filters[t]
filters=[img, imgBlur, imgFiltered, imgGB, imgM, imgL, imgH]
Filters=['Raw image', 'Blur', 'Custom filter','Gaussian blur', 'Morph', 'Laplacian', 'Harris corner']
cv2.namedWindow('input',cv2.WINDOW_NORMAL)
cv2.namedWindow('flow',cv2.WINDOW_NORMAL)
cv2.createTrackbar('filter', 'flow', 0, 6, nada3)
while True:
	base_image=cv2.getTrackbarPos('filter', 'flow')
	Img=filters[base_image]	
	h, w = Img.shape[:2]	
	eigen = cv2.cornerEigenValsAndVecs(Img, 15, 3)
	eigen = eigen.reshape(h, w, 3, 2)  # [[e1, e2], v1, v2]
	flow = eigen[:,:,2]

	vis = Img.copy()
	vis[:] = (192 + np.uint32(vis)) / 2
	d = 12
	points =  np.dstack( np.mgrid[d/2:w:d, d/2:h:d] ).reshape(-1, 2)
	for x, y in points:
   		vx, vy = np.int32(flow[y, x]*d)
		cv2.line(vis, (x-vx, y-vy), (x+vx, y+vy), (0, 0, 0), 1, cv2.CV_AA)
	
	cv2.imshow('input', Img)
	cv2.imshow('flow', vis)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break


cv2.destroyAllWindows()


cv2.waitKey(0)
