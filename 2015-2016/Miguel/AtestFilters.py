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

data, header = fits.getdata(fitsFileI, header=True)
hdu_list = fits.open(dataset[sys.argv[1]])
img = hdu_list[0].data
Min=np.amin(img)
Max=np.amax(img)
img = 255*(img+abs(Min))/Max

cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.imshow('img',img)

imgBlur = cv2.blur(img,(3,3))


imgFiltered=cv2.filter2D(img,-1,np.array([[0,1,0],[1,0,1],[0,1,0]]))


imgGB=cv2.GaussianBlur(img,(3,3),1)

imgM=cv2.morphologyEx(img, cv2.MORPH_GRADIENT,(3,3))


imgL=cv2.Laplacian(img,-1)


imgS=cv2.Sobel(img,-1,3,2,ksize=5)



imgH=cv2.cornerHarris(img,3,3,0.0005)


row1 = np.concatenate((img, imgBlur, imgFiltered),axis=1)
row2 = np.concatenate((imgGB, imgM, imgL),axis=1)
row3 = np.concatenate((imgS, imgH,np.zeros(img.shape)),axis=1)
img_collage=np.concatenate((row1,row2,row3),axis=0)

cv2.putText(img_collage,'Base image',(2048*2+10,1489*2+250), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,255),2)
cv2.putText(img_collage,'Blur',(7*2048/3+10,1489*2+250), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,255),2)
cv2.putText(img_collage,'Custom filter',(8*2048/3+10,1489*2+250), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,255),2)

cv2.putText(img_collage,'Gaussian blur',(2048*2+10,7*1489/3+250), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,255),2)
cv2.putText(img_collage,'Morphological',(7*2048/3+10,7*1489/3+250), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,255),2)
cv2.putText(img_collage,'Laplacian',(8*2048/3+10,7*1489/3+250), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,255),2)

cv2.putText(img_collage,'Sobel',(2048*2+10,8*1489/3+250), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,255),2)
cv2.putText(img_collage,'Harris',(7*2048/3+10,8*1489/3+250), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,255,255),2)


cv2.line(img_collage,(2048,0),(2048,1489*3),(255,255,255),2)
cv2.line(img_collage,(7*2048/3,1489*2),(7*2048/3,1489*3),(255,255,255),2)

cv2.line(img_collage,(2048*2,0),(2048*2,1489*3),(255,255,255),2)
cv2.line(img_collage,(8*2048/3,1489*2),(8*2048/3,1489*3),(255,255,255),2)

cv2.line(img_collage,(0,1489),(2048*3,1489),(255,255,255),2)
cv2.line(img_collage,(2048*2,7*1489/3),(2048*3,7*1489/3),(255,255,255),2)

cv2.line(img_collage,(0,1489*2),(2048*3,1489*2),(255,255,255),2)
cv2.line(img_collage,(2048*2,8*1489/3),(2048*3,8*1489/3),(255,255,255),2)


cv2.namedWindow("Image collage", cv2.WINDOW_NORMAL)
cv2.imshow("Image collage", img_collage)
cv2.waitKey()


def nada(x):
	print x/100.
def nada2(t):
	print "Threshold used:", Thresholds[t]
def nada3(t):
	print "Filter used as base image:", Filters[t]
cv2.namedWindow("binary", cv2.WINDOW_NORMAL)
cv2.createTrackbar('thresh', 'binary', 100, 200, nada)
thresholds=[cv2.THRESH_BINARY,cv2.THRESH_BINARY_INV,cv2.THRESH_TRUNC,cv2.THRESH_TOZERO,cv2.THRESH_TOZERO_INV]
Thresholds=['Binary', 'Binary_inv', 'Trunc', 'Tozero','Tozero_inv']
filters=[img, imgBlur, imgFiltered, imgGB, imgM, imgL, imgH]
Filters=['Raw image', 'Blur', 'Custom filter','Gaussian blur', 'Morph', 'Laplacian', 'Harris corner']
nada2(0)
nada3(0)
cv2.createTrackbar('threshold type', 'binary', 1, 4, nada2)
cv2.createTrackbar('filter', 'binary', 2, 6, nada3)
max_area=0
X,Y,W,H=0,0,0,0
while True:
	thresh=cv2.getTrackbarPos('thresh', 'binary')
	threshold=cv2.getTrackbarPos('threshold type', 'binary')
	base_image=cv2.getTrackbarPos('filter', 'binary')
	_,binary=cv2.threshold(filters[base_image], cv2.THRESH_OTSU, thresh/100., thresholds[threshold])
	contours, _ = cv2.findContours(cv2.convertScaleAbs(binary),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(binary,contours,-1,(0,0,0),1)
	cv2.namedWindow("binary", cv2.WINDOW_NORMAL)
	for cnt in contours:
		x,y,w,h = cv2.boundingRect(cnt)
		X,Y,W,H,max_area = (x,y,w,h,w*h) if w*h>max_area and w*h<2040*1480 else (X,Y,W,H,max_area)
		cv2.rectangle(binary,(x,y),(x+w,y+h),(0,0,0),1)
		rect = cv2.minAreaRect(cnt)
		box = cv2.cv.BoxPoints(rect)
		box = np.int0(box)
		im = cv2.drawContours(binary,[box],0,(0,0,0),1)
	cv2.imshow("binary",binary)
	#cv2.imwrite('binarytest{}.png'.format(sys.argv[1]),255* binary)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

print X,Y,W,H,max_area
cv2.namedWindow("crop",cv2.WINDOW_NORMAL)
cropped=binary[Y:Y+H,X:X+W]
while True:
    cv2.rectangle(img,(X,Y),(X+W,Y+H),(0,255,0),2)
    cv2.imshow('img',255*binary)
    #cv2.imwrite('binaryWrectangletest{}.png'.format(sys.argv[1]),255*binary)
    cv2.imshow('crop',255*cropped)
    #cv2.imwrite('croppedtest{}.png'.format(sys.argv[1]),cv2.convertScaleAbs(255*cropped))
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
		break
cv2.destroyAllWindows()
