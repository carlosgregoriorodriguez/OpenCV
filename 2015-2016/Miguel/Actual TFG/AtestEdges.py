# -*- coding: utf-8 -*-
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cv2
import sys
import numpy as np

fitsFileI="../TFG/frame-i-004264-4-0259.fits" #m81 http://mirror.sdss3.org/fields/name?name=m81
fitsFileU="../TFG/frame-u-004264-4-0259.fits" #m81
fitsFileR="../TFG/frame-r-004264-4-0259.fits" #m81 
fitsFileG="../TFG/frame-g-004264-4-0259.fits" #m81
f1="../TFG/f1.jpg"
fitsFileI2="../TFG/frame-i-003804-6-0084.fits" #m66 http://mirror.sdss3.org/fields/name?name=m66
fitsFileU2="../TFG/frame-u-003804-6-0084.fits" #m66
fitsFileR2="../TFG/frame-r-003804-6-0084.fits" #m66
fitsFileG2="../TFG/frame-g-003804-6-0084.fits" #m66
fitsFileI3='../TFG/frame-i-004381-2-0120.fits' #m91 http://mirror.sdss3.org/fields/name?name=m91
fitsFileI4='../TFG/frame-i-002830-6-0398.fits' #m109 http://mirror.sdss3.org/fields/name?name=m109
fitsFileI5='../TFG/frame-i-003805-2-0023.fits' #m59 http://mirror.sdss3.org/fields/name?name=m59
fitsFileI6='../TFG/frame-i-008112-2-0074.fits' #m33 http://mirror.sdss3.org/fields/name?name=m33
fitsFileI7='../TFG/frame-i-007845-2-0104.fits' #m74 http://mirror.sdss3.org/fields/name?name=m74
fitsFileI8='../TFG/frame-i-003836-4-0084.fits' #m95 http://mirror.sdss3.org/fields/name?name=m95
dataset={'i':fitsFileI,'u':fitsFileU,'r':fitsFileR,'g':fitsFileG,'1':f1,'i2':fitsFileI2,'u2':fitsFileU2,'r2':fitsFileR2,'g2':fitsFileG2,'i3':fitsFileI3,'i4':fitsFileI4,'i5':fitsFileI5,'i6':fitsFileI6,'i7':fitsFileI7,'i8':fitsFileI8}

data = fits.getdata(dataset[sys.argv[1]])
hdu_list = fits.open(dataset[sys.argv[1]])
img = hdu_list[0].data
Min=np.amin(img)
Max=np.amax(img)
img = 255*(img+abs(Min))/Max
imgGB = cv2.GaussianBlur(img,(3,3),0)
_,img=cv2.threshold(img, cv2.THRESH_OTSU, 20, cv2.THRESH_TOZERO_INV)


sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)  # x
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)  # y

plt.subplot(2,2,1),plt.imshow(img,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

grad=cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0);
cv2.namedWindow("Combination", cv2.WINDOW_NORMAL)
cv2.imshow("Combination",grad)
cv2.waitKey(0)
plt.show()
