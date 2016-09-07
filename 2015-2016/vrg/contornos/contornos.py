import numpy as np
import cv2

def erode(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		erosion = cv2.erode(img,kernel,iterations = 1)
		return erosion
def closeContour(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		closeResult = cv2.morphologyEx(img,cv2.MORPH_OPEN, kernel)
		return closeResult

def dilate(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		dilateResult = cv2.dilate(img,kernel,iterations = 1)
		return dilateResult

im = dilate(closeContour(cv2.imread('test3.png'), 10),6)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,200,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print len(contours)
cv2.drawContours(im, contours, -1, (0,0,128), 1) 
cv2.imshow("Original", im)
cv2.waitKey(0)