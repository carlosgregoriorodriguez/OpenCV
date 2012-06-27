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
	
		layer = cv2.merge([layer,]*3)
		canvas[:,:,:]=canvas[:,:,:]+layer
	return canvas


def identifyLevels(probMask):
	canvas = np.zeros((probMask.shape[0],probMask.shape[1],3),np.uint8)
	maxVal = cv2.minMaxLoc(probMask)[1]
	step = int(maxVal/5)

	for i in range(5):
		interval = (i*step,(i+1)*step)
		if i == 0:
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*50
			layer = cv2.merge([layer,]*3)
			canvas[:,:,:]=canvas[:,:,:]+layer
		elif i == 4:
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*255
			layer = cv2.merge([layer,]*3)
			canvas[:,:,:]=canvas[:,:,:]+layer
		else:
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*255
			canvas[:,:,i-1]=canvas[:,:,i-1]+layer

	return canvas


def findSpotsInRed(original,mask,levelNumber,level):

	redChannel = cv2.min(mask,cv2.split(original)[0])
	redChannel,contByLvl,imageList = greyValueSegmentation(redChannel,levelNumber)
	

	# rawContours,hierarchy = cv2.findContours(redChannel.copy(),
	# 	cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	# bigCont = []
	# if len(rawContours)>0:
	# 	for cnt in zip(hierarchy[0],rawContours):
	# 		#contornos que (no tengan hijos o tengan hermano izquierdo) y no sean unipuntuales
	# 		#print cnt[0]
	# 		#if (cnt[0][2]<0 or cnt[0][0]>-1) and len(cnt[1])>1:
	# 		if len(cnt[1])>1:
	# 			bigCont.append(cv2.approxPolyDP(cnt[1],3,True))
	#cv2.drawContours(original,bigCont,-1,(0,255,0),2)
	
	redChannel = cv2.merge([np.clip(imageList[level],0,1)*255,]*3)

	#redChannel = cv2.merge([redChannel,]*3)
	
	cv2.drawContours(redChannel,contByLvl[level],-1,(0,255,0),2)
	
	#return original
	return redChannel
	


def findColorMarks(img,mask):
	cuttedImg = cv2.merge([cv2.min(mask,layer) for layer in cv2.split(img)])
	print '-FINDSPOT-findColorMarks'
	cuttedImgBP = getHistRGB(cuttedImg,mask)
	cuttedImgBP = cv2.min(cuttedImgBP,mask)
	#return cv2.merge([cuttedImgBP,]*3)
	return identifyLevels(cuttedImgBP)

def getBlueMask(img,mask):
	blueChannel = cv2.min(mask,cv2.split(img)[0])
	return cv2.merge([blueChannel,]*3)
	
if __name__ == "__main__":

	print 'only methods'































