import cv2
import numpy as np
import sys
from glob import glob

def thresholdChannels(img):
	mergeAux=[]
	for channel in cv2.split(img):
		mergeAux.append(cv2.threshold(channel,180,255,cv2.cv.CV_THRESH_BINARY)[1])
	
	aux = cv2.min(mergeAux[0],mergeAux[1])
	aux = cv2.min(aux,mergeAux[2])
	return cv2.merge([aux]*3)

if __name__ == "__main__":
	
	path = '../images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])
	img = cv2.resize(img,(min(img.shape[1],1250),min(img.shape[0],750)))
	
	threshImg = thresholdChannels(img)
	
	
	while True:	

		cv2.imshow('original',img)
		cv2.imshow('thresholded',threshImg)

		key = cv2.waitKey(5)
	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
	 		img = cv2.resize(img,(min(img.shape[1],1250),min(img.shape[0],750)))
			threshImg = thresholdChannels(img)	 		
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])
	 		img = cv2.resize(img,(min(img.shape[1],1250),min(img.shape[0],750)))
			threshImg = thresholdChannels(img)	 		
	 	elif (key != -1):
	 		break

























