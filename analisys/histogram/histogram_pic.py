import cv2
import numpy as np

img = cv2.imread('../../img/beach.jpg')
h = np.zeros((300,255,3))
b,g,r = cv2.split(img)
bins = np.arange(256).reshape(256,1)
color = [ (255,0,0),(0,255,0),(0,0,255) ]


for item,col in zip([b,g,r],color):
	hist_item = cv2.calcHist([item],[0],None,[256],[0,255])
	
	cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)

	hist=np.int32(np.around(hist_item))

	pts = np.column_stack((bins,hist))

	cv2.polylines(h,np.array([pts],np.int32),False,col)
	
h=np.flipud(h)

cv2.imshow('colorhist',h)
cv2.waitKey(0)