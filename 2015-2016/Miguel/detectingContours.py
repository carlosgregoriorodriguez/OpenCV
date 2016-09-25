from astropy.io import fits
import cv2
import numpy as np

fitsFile="../examples/Filters/frame-i-002830-6-0398.fits"
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
cv2.drawContours(binary,contours,-1,(0,255,0),2)

cv2.namedWindow("binary", cv2.WINDOW_NORMAL)
cv2.imshow("binary",binary)
cv2.waitKey()
