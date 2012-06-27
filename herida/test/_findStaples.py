import cv2
import numpy as np


#Methods for finding up staples in a 3-channel image
#All methods return a single channel, 8 bit image of the same size as the given image 

#Applies consecutively blur and adaptative threshold to the given image
def blurAndAT(img,blatList):
	
	iterations = blatList[0]+1
	ksizeB = (blatList[1][0]+1,blatList[1][1]+1)
	ksizeAT = 2*blatList[2]+3

	bwImg = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)
	
	for i in range(iterations):
		bwImg = cv2.blur(bwImg,ksizeB)
		bwImg = cv2.adaptiveThreshold(bwImg, 255,
			cv2.cv.CV_ADAPTIVE_THRESH_MEAN_C, 
			cv2.cv.CV_THRESH_BINARY, ksizeAT, 20)
	return bwImg


def thresholdChannels(img,thresh):
	mergeAux=[]
	for channel in cv2.split(img):
		mergeAux.append(cv2.threshold(channel,thresh,255,cv2.cv.CV_THRESH_BINARY)[1])	
	aux = cv2.min(mergeAux[0],mergeAux[1])
	aux = cv2.min(aux,mergeAux[2])
	return aux


def simpleCanny(img,cannyList):
	return cv2.Canny(cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY), cannyList[0], cannyList[1])




if __name__ == "__main__":
	print 'only methods'









	
