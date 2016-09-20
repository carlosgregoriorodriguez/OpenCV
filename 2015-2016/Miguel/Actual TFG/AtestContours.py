from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import cv2
import sys
import numpy as np
num=8
fitsFileI1="../TFG/frame-i-004264-4-0259.fits" #m81 http://mirror.sdss3.org/fields/name?name=m81
fitsFileI2="../TFG/frame-i-003804-6-0084.fits" #m66 http://mirror.sdss3.org/fields/name?name=m66
fitsFileI3='../TFG/frame-i-004381-2-0120.fits' #m91 http://mirror.sdss3.org/fields/name?name=m91
fitsFileI4='../TFG/frame-i-002830-6-0398.fits' #m109 http://mirror.sdss3.org/fields/name?name=m109
fitsFileI5='../TFG/frame-i-003805-2-0023.fits' #m59 http://mirror.sdss3.org/fields/name?name=m59
fitsFileI6='../TFG/frame-i-008112-2-0074.fits' #m33 http://mirror.sdss3.org/fields/name?name=m33
fitsFileI7='../TFG/frame-i-007845-2-0104.fits' #m74 http://mirror.sdss3.org/fields/name?name=m74
fitsFileI='../TFG/frame-i-003836-4-0084.fits' #m95 http://mirror.sdss3.org/fields/name?name=m95
if len(sys.argv)<2:
	fitsFile=fitsFileI
else:
	fitsFile=sys.argv[1]
data = fits.getdata(fitsFile)
hdu_list = fits.open(fitsFile)
img = hdu_list[0].data
Min=np.amin(img)
Max=np.amax(img)
img = 255*(img+abs(Min))/Max
imgFiltered=cv2.filter2D(img,-1,np.array([[0,1,0],[1,0,1],[0,1,0]]))
#imgFiltered=cv2.GaussianBlur(img,(3,3),-1)
_,imgBase=cv2.threshold(imgFiltered, cv2.THRESH_OTSU, 1.5, cv2.THRESH_BINARY_INV)
#_,imgBase=cv2.threshold(imgFiltered, cv2.THRESH_OTSU, 0, cv2.THRESH_TOZERO_INV)
cv2.namedWindow('Base image', cv2.WINDOW_NORMAL)
cv2.imshow('Base image', img)
cv2.imwrite('testhdu{}.png'.format(num),255*hdu_list[0].data)
cv2.imwrite('testimg{}.png'.format(num),255*img)
cv2.imwrite('testimgFiltered{}.png'.format(num),255*imgFiltered)
cv2.imwrite('testimgBase{}.png'.format(num),255*imgBase)


#imgProcessed = cv2.convertScaleAbs(cv2.morphologyEx(imgBase, 0, (3,3),iterations=12))
#h, w = imgProcessed.shape[:2]
#print imgProcessed.shape,imgProcessed.dtype
#cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#cv2.imshow('image', imgProcessed*255) 

h, w = imgBase.shape[:2]
contours, hierarchy = cv2.findContours(cv2.convertScaleAbs(imgBase),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#_,binary=cv2.threshold(cv2.blur(img,(3,3)), cv2.THRESH_OTSU, 100, cv2.THRESH_TRUNC)
#contours, hierarchy = cv2.findContours(cv2.convertScaleAbs(binary),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cv2.imshow('Base image', binary)

'''
test=np.array(hierarchy)
print test.shape
print test[0]
print test[0].shape

perimeters=np.array(map(lambda x:cv2.arcLength(x,True),contours))
print perimeters.shape
m=np.argmax(perimeters,axis=0)
print "m:",m
M=contours[m]
print cv2.arcLength(contours[m],True),m,M,M.shape
'''
def update(levels):
    vis = np.zeros((h, w, 3), np.uint8)
    levels = levels - 3
    cv2.namedWindow('contours', cv2.WINDOW_NORMAL)
    cv2.drawContours( vis, contours, (-1, 3)[levels <= 0], (255,255,255), 1, cv2.CV_AA, hierarchy, abs(levels))
    cv2.imshow('contours',vis)
    #cv2.imwrite('test.png', vis)
update(3)
cv2.namedWindow('contours', cv2.WINDOW_NORMAL)
#cv2.namedWindow('contours2', cv2.WINDOW_NORMAL)
#vis = np.zeros((h, w, 3), np.uint8)
#cv2.drawContours(vis, M, -1, (255,255,255), 2, cv2.CV_AA)#, 0, 2)
#cv2.imshow('contours2',vis)
#cv2.imwrite('a.jpeg', imgProcessed)
cv2.createTrackbar( "levels+3", "contours", 3, 7, update)
cv2.imshow('contours', imgBase)

0xFF & cv2.waitKey()
cv2.destroyAllWindows()
