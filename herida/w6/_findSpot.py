import cv2
import numpy as np
from _utils import *
from _fleshBackProyection import *

def getContoursInFlesh(img,mask):
	

	rawContours,hierarchy = cv2.findContours(mask.copy(),
		cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	bigCont = [] #contours with more than one element
	for cnt in rawContours:
		if len(cnt)>1:
			cvxH = cv2.convexHull(cnt)
			area = cv2.contourArea(cvxH,False)
			if area>10:
				bigCont.append(cvxH)
	return bigCont


def floodfillContours(img,mask):
	if len(contours)>0:
		hi = 5
		lo = 5
		aux = np.zeros((img.shape[0]+2,img.shape[1]+2),np.uint8)
		for cont in enumerate(contours):
			center = cv2.minEnclosingCircle(cont)[0]
			cv2.floodFill(img, aux, center, [255,0,0],[lo,]*3,[hi,]*3,cv2.cv.CV_FLOODFILL_FIXED_RANGE)
	return img


def bpContours(img,mask):
	#mask = np.ones(mask.shape,np.uint8)*255-mask
	contours = getContoursInFlesh(img,mask)
	print contours
	print len(contours)
	if len(contours)>0:
		#cv2.drawContours(img,contours,-1,(0,0,255),-1)
		
		for cont in enumerate(contours):

			
			rectPoints = cv2.boundingRect(cont[1])
			cv2.rectangle(img,(rectPoints[0],rectPoints[1]),
				(rectPoints[0]+rectPoints[2],rectPoints[1]+rectPoints[3]),
				(0,255,0),2)
			
			#auxRect = img[:,:,:]
			#hist = getHist(auxRect)
			#bpImg = cv2.calcBackProject([img],[0,1], hist, [0,180,0,256],1)
	return img


if __name__ == "__main__":

	print 'only methods'































