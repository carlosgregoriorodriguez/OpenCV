# -*- coding: utf-8 -*-
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cv2
import sys
import numpy as np



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
img = hdu_list[0].data
Min=np.amin(img)
Max=np.amax(img)
img = 255*(img+abs(Min))/Max


imgBlur = cv2.blur(img,(3,3))


imgFiltered=cv2.filter2D(img,-1,np.array([[0,1,0],[1,0,1],[0,1,0]]))


imgGB=cv2.GaussianBlur(img,(3,3),1)


imgM=cv2.morphologyEx(img, cv2.MORPH_GRADIENT,(3,3))

imgL=cv2.Laplacian(img,-1)


imgS=cv2.Sobel(img,-1,3,2,ksize=5)



imgH=cv2.cornerHarris(img,3,3,0.0005)


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
