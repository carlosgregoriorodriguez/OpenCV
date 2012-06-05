import cv2
import numpy as np
import sys
from glob import glob
import math
from _findStaples import *
from _getContours import *
from _squareHistogram import *
from _fleshBackProyection import *

def dummy(x):
	global changeParam
	changeParam = True
	print x

def stapleContThresh(img,dirList,thresh):
	threshChan = thresholdChannels(img,thresh)
	return stapleCont(threshChan,dirList)

def stapleContCanny(img,dirList,cannyList):
	threshChan = simpleCanny(img,cannyList)
	return stapleCont(threshChan,dirList)

def stapleContBlurAT(img,dirList,blatList):
	threshChan = blurAndAT(img,blatList)
	return stapleCont(threshChan,dirList)

def doAndPack(img,dirList,thresh,cannyList,blatList,relevanceThresh,probThresh):
	h, w = 375,450

	auxImg = cv2.equalizeHist(cv2.cvtColor(img,cv2.cv.CV_BGR2GRAY))
	eqImg = cv2.merge([auxImg,]*3)
	backEqImg = cv2.cvtColor(auxImg,cv2.cv.CV_GRAY2BGR)

	aux = []
	aux.append(stapleContCanny(backEqImg,dirList,cannyList))
	aux.append(stapleContThresh(backEqImg,dirList,thresh))
	aux.append(stapleContBlurAT(backEqImg,dirList,blatList))

	
	cpImg0,cpImg1,cpImg2 = backEqImg.copy(),backEqImg.copy(),backEqImg.copy()

	cv2.drawContours(cpImg0, aux[0], -1, (0,0,255),2)
	cv2.drawContours(cpImg1, aux[1], -1, (0,0,255),2)
	cv2.drawContours(cpImg2, aux[2], -1, (0,0,255),2)

	img5,sqHist5 = getSigSquares(aux,img.shape,(10,10),relevanceThresh)

	img5 = cv2.merge([cv2.min(img5,layer) for layer in cv2.split(img)])

	bp5 = bpSignificantSquares(img.copy(),sqHist5,probThresh)
	#bp25 = bpSignificantSquares(img.copy(),sqHist25,probThresh)

	

	background = np.zeros((h*2,w*3,3),np.uint8)
	#background[0:h,0:w,0:3]=cv2.resize(img,(w,h))
	background[0:h,0:w,0:3]=cv2.resize(backEqImg,(w,h))
	background[0:h,w:2*w,0:3]=cv2.resize(img5,(w,h))
	background[0:h,2*w:3*w,0:3]=cv2.resize(bp5,(w,h))
	
	background[h:2*h,0:w,0:3]=cv2.resize(cpImg0,(w,h))
	background[h:2*h,w:2*w,0:3]=cv2.resize(cpImg1,(w,h))
	background[h:2*h,2*w:3*w,0:3]=cv2.resize(cpImg2,(w,h))
	return background





if __name__ == "__main__":
	print 'this script finds all the contours of a'
	print 'specified area and orientation and cuts'
	print 'the tiles containing them out of the original image'
	print 'not connected tiles are blended'
	print ''
	print 'use z and x to move through the images'

	path = '../images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])	
	
	cv2.namedWindow('panel',cv2.cv.CV_WINDOW_NORMAL)
	cv2.namedWindow('panel canny',cv2.cv.CV_WINDOW_NORMAL)
	cv2.namedWindow('panel blat',cv2.cv.CV_WINDOW_NORMAL)
	cv2.namedWindow('panel direction',cv2.cv.CV_WINDOW_NORMAL)
	cv2.createTrackbar('minArea','panel direction',0,500,dummy)
	cv2.createTrackbar('maxArea','panel direction',5000,5000,dummy)
	cv2.createTrackbar('direction','panel direction',5,5,dummy)
	cv2.createTrackbar('canny thresh1','panel canny',700,700,dummy)
	cv2.createTrackbar('canny thresh2','panel canny',700,700,dummy)
	cv2.createTrackbar('thresh','panel',180,255,dummy)
	cv2.createTrackbar('iterations','panel blat',1,10,dummy)
	cv2.createTrackbar('ksizeBlur X','panel blat',0,4,dummy)
	cv2.createTrackbar('ksizeBlur Y','panel blat',0,4,dummy)
	cv2.createTrackbar('ksizeAT','panel blat',0,4,dummy)
	cv2.createTrackbar('relevanceThresh','panel',0,3,dummy)
	cv2.createTrackbar('probThresh','panel',1,256,dummy)

	dirList = [cv2.getTrackbarPos('minArea','panel direction'),
		cv2.getTrackbarPos('maxArea','panel direction'),
		cv2.getTrackbarPos('direction','panel direction')]
	
	cannyList = [cv2.getTrackbarPos('canny thresh1','panel canny'),
		cv2.getTrackbarPos('canny thresh2','panel canny')]

	blatList = [cv2.getTrackbarPos('iterations','panel blat'),
		(cv2.getTrackbarPos('ksizeBlur X','panel blat'),cv2.getTrackbarPos('ksizeBlur Y','panel blat')),
		cv2.getTrackbarPos('ksizeAT','panel blat')]

	changeParam = False

	bigImg = doAndPack(img,dirList,
		cv2.getTrackbarPos('thresh','panel'),
		cannyList,blatList,
		cv2.getTrackbarPos('relevanceThresh','panel'),
		cv2.getTrackbarPos('probThresh','panel')
		)


	while True:
		if changeParam:
			dirList = [cv2.getTrackbarPos('minArea','panel direction'),
				cv2.getTrackbarPos('maxArea','panel direction'),
				cv2.getTrackbarPos('direction','panel direction')]
		
			cannyList = [cv2.getTrackbarPos('canny thresh1','panel canny'),
				cv2.getTrackbarPos('canny thresh2','panel canny')]

			blatList = [cv2.getTrackbarPos('iterations','panel blat'),
				(cv2.getTrackbarPos('ksizeBlur X','panel blat'),cv2.getTrackbarPos('ksizeBlur Y','panel blat')),
				cv2.getTrackbarPos('ksizeAT','panel blat')]

			bigImg = doAndPack(img,dirList,
				cv2.getTrackbarPos('thresh','panel'),
				cannyList,blatList,
				cv2.getTrackbarPos('relevanceThresh','panel'),
				cv2.getTrackbarPos('probThresh','panel')
			)
			changeParam = False

		cv2.imshow('original',bigImg)

		key = cv2.waitKey(5)
	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
	 		changeParam = True
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])
	 		changeParam = True
	 	elif (key != -1):
	 		break









	
