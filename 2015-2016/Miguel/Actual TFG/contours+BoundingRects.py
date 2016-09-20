# -*- coding: utf-8 -*-
from astropy.io import fits
import cv2
import numpy as np

fitsFile="../TFG/frame-i-002830-6-0398.fits"
hdulist = fits.open(fitsFile)
img = hdulist[0].data


Min=abs(np.amin(img))
Max=np.amax(img)
img = 255*(img+Min)/Max
imgFiltered=cv2.filter2D(img,-1,np.array([[0,1,0],[1,0,1],[0,1,0]]))

_,binary=cv2.threshold(imgFiltered, cv2.THRESH_OTSU, 1.0, cv2.THRESH_BINARY_INV)
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image",binary)
cv2.waitKey()
contours, _ = cv2.findContours(cv2.convertScaleAbs(binary),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(binary,contours,-1,(0,0,0),2) #Este método dibuja los contornos en la imagen binary

cv2.namedWindow("Contours with bounding rectangles", cv2.WINDOW_NORMAL)

max_area=1
X,Y,W,H=0,0,0,0
for cnt in contours:
	x,y,w,h = cv2.boundingRect(cnt)
	X,Y,W,H,max_area = (x,y,w,h,w*h) if w*h>max_area and w*h<2040*1480 else (X,Y,W,H,max_area)
	cv2.rectangle(binary,(x,y),(x+w,y+h),(0,0,0),1) #Este método dibuja los rectángulos que ajustan los contornos en la imagen binary
cv2.imshow("Contours with bounding rectangles",binary)
cv2.waitKey()
cv2.imwrite("img3.png",255*binary)
cropped=binary[Y:Y+H,X:X+W]
cv2.imshow('crop',255*cropped)
cv2.imwrite("img3Rect.png", 255*cropped)
cv2.waitKey()
