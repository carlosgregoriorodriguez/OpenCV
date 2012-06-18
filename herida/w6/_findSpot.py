import cv2
import numpy as np
from _utils import *
from _fleshBackProyection import *

def getContoursInFlesh(img,mask):
	print '-FINDSPOT-getContours'

	rawContours,hierarchy = cv2.findContours(mask.copy(),
		cv2.cv.CV_RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

	print '-FINDSPOT-rawContour'
	#print rawContours
	print '-FINDSPOT-hierarchy'
	print hierarchy
	print len(rawContours)
	bigCont = [] #contours with more than one element
	for cnt in zip(hierarchy[0],rawContours):
		#print cnt
		#todos los contornos que no tengan hijos (cnt[0][2]<0) y tengan padre (cnt[0][3]>-1)
		if cnt[0][2]<0 and cnt[0][3]>-1:
			if len(cnt[1])>1:
				cvxH = cv2.convexHull(cnt[1])
				area = cv2.contourArea(cvxH,False)
				if area>5:
					bigCont.append(cvxH)
	print bigCont
	return bigCont


def getHistRGB(img,mask):
	imgArray = [img,]
	channels = [0,1]
	histSize = [128,128]
	ranges = [0,256,0,256]
	hist = cv2.calcHist(imgArray,channels,mask,histSize,ranges) 
	aux = cv2.calcBackProject(imgArray,[0,1], hist, [0,256,0,256],1)
	return aux


def markColors(probMask):
	canvas = np.zeros((probMask.shape[0],probMask.shape[1],3),np.uint8)
	maxVal = cv2.minMaxLoc(probMask)[1]
	step = 40

	for i in range(0,int(maxVal/step)):
		if i == int(maxVal/step)-1:
			interval = (i*step,maxVal)
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*maxVal
			
		else:
			interval = (i*step,(i+1)*step)
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*i*step
			canvas[:,:,i%3]=canvas[:,:,i%3]+layer
		layer = cv2.merge([layer,]*3)
		canvas[:,:,:]=canvas[:,:,:]+layer
	return canvas


def findColorMarks(img,mask):
	cuttedImg = cv2.merge([cv2.min(mask,layer) for layer in cv2.split(img)])
	print '-FINDSPOT-findColorMarks'
	cuttedImgBP = getHistRGB(cuttedImg,mask)
	cuttedImgBP = cv2.min(cuttedImgBP,mask)
	#return cv2.merge([cuttedImgBP,]*3)
	return markColors(cuttedImgBP)





# def bpContours(img,mask):
# 	contours = getContoursInFlesh(img,mask)
# 	print contours
# 	print len(contours)
# 	if len(contours)>0:		
# 		for cont in enumerate(contours):
# 			rectPoints = cv2.boundingRect(cont[1])
# 			cv2.rectangle(img,(rectPoints[0],rectPoints[1]),
# 				(rectPoints[0]+rectPoints[2],rectPoints[1]+rectPoints[3]),
# 				(0,255,0),2)
# 	return img

if __name__ == "__main__":

	print 'only methods'































