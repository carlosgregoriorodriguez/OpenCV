import cv2
import numpy as np
import sys
from glob import glob
import math
from time import clock
import pickle
from _utils import *
from _findStaples import *
from _getContours import *
from _squareHistogram import *
from _fleshBackProyection import *
from _findSpot import *

def dummy(x):
	global changeParam
	changeParam = True
	changeSeed = True
	print x

def dummy2(x):
	global changeSeed
	changeSeed = True
	print x

def fillHistogram(img,seedPoint,histogram):
	print 'histogram len '+str(len(histogram))
	aux = cv2.split(img)[0]
	newVal = (255,255,255)
	for i in range(1,11,2):
		for j in range(1,11,2):
			loDiff = [i,]*3
			upDiff = [j,]*3
			mask = np.zeros((img.shape[0]+2,img.shape[1]+2),np.uint8)
			#mask[1:img.shape[0]+1,1:img.shape[1]+1]=aux
			cv2.floodFill(img.copy(), mask, seedPoint, newVal, loDiff, upDiff,cv2.FLOODFILL_FIXED_RANGE)
			print 'integralValue '+str(integralValue(mask))
			print histogram[integralValue(mask)]
			histogram[integralValue(mask)]+=1
			print histogram[integralValue(mask)]
	# for i in histogram:
	# 	if histogram[i]>0:
	# 		print str(histogram[i])+' elements with area '+str(i)
	#print histogram
	return histogram



def findBreakingPoint(img,seedPoint):
	#idea, ir de 1 en 1 en los dos parametros a la vez, ahi la pendiente o la relacion de areas
	#si es significativa => encontramos breakingpoint (a,b) y luego ya solo tenemos que buscar
	#el maximo en el area de todos los pares (c,d) con c<=a o d<=b sabiendo que el area tiene que
	#estar mas cerca del area de (a,b) que del area de (a+1,b+1)
	upDiff = [0,]*3
	loDiff = [0,]*3
	newVal = (255,255,255)
	median = 0
	lastMedian = 0
	maxIntegral = integralValue(np.ones((img.shape[0]+2,img.shape[1]+2),np.uint8)*255)
	print 'FINDBREAKINGPOINT'
	print 'maxIntegral '+str(maxIntegral)
	for i in range(1,50,2):
		loDiff = [i,]*3
		mask = np.zeros((img.shape[0]+2,img.shape[1]+2),np.uint8)
		cv2.floodFill(img.copy(), mask, seedPoint, newVal, loDiff, upDiff,cv2.FLOODFILL_FIXED_RANGE)
		print 'integralValue '+str(integralValue(mask))
		if not lastMedian:
			lastMedian = median
			median = (median*(i-1)+integralValue(mask))/i
		else:
			median = (median*(i-1)+integralValue(mask))/i
			lastMedian = median
		print loDiff
		print 'new iteration '+str(i)
		print 'lastmedian '+str(lastMedian)
		print 'median '+str(median)
		if (median>2*lastMedian) and (i>1):
			loDiff =  [i-2,]*3
			break
	print 'UPDIFF'
	median = 0
	lastMedian = 0
	for i in range(1,50,2):
		upDiff = [i,]*3
		mask = np.zeros((img.shape[0]+2,img.shape[1]+2),np.uint8)
		cv2.floodFill(img.copy(), mask, seedPoint, newVal, loDiff, upDiff,cv2.FLOODFILL_FIXED_RANGE)
		print 'integralValue '+str(integralValue(mask))
		if i!=1:
			lastMedian = median
			median = (median*(i-1)+integralValue(mask))/i
		if i ==1:
			median = (median*(i-1)+integralValue(mask))/i
			lastMedian = median
		print upDiff
		print 'new iteration '+str(i)
		print 'lastmedian '+str(lastMedian)
		print 'median '+str(median)
		if median>1.2*lastMedian and i>1:
			upDiff =  [i-2,]*3
			break
	print 'calculados loDiff y upDiff'
	print loDiff
	print upDiff
	return loDiff,upDiff




def doAndPack(img,dirList,thresh,cannyList,blatList,relevanceThresh,probThresh):
	print 'NEW IMAGE'
	print 'current time: '+str(clock())

	h, w = 375,450
	
	#get different formats of the original image	
	aux = []
	for channel in cv2.split(img):
		aux.append(cv2.equalizeHist(channel))

	backEqImg = cv2.merge(aux)
	
	#apply the image in the format that suits best to the different algorithms 
	aux = []
	print 'BEFORE GETTING THE CONTOURS'
	myTime = clock()
	print 'first contour at: '+str(clock())
	aux.append(stapleContCanny(backEqImg,dirList,cannyList))
	print '====>takes '+str(clock()-myTime)
	myTime = clock()
	print 'second contour at: '+str(clock())
	aux.append(stapleContThresh(img,dirList,thresh))
	print '====>takes '+str(clock()-myTime)
	myTime = clock()
	print 'third contour at: '+str(clock())
	aux.append(stapleContBlurAT(backEqImg,dirList,blatList))
	print '====>takes '+str(clock()-myTime)
	myTime = clock()


	#get the squareHistogram for all the contours, see _squareHistogram.getSigSquare
	print 'get significant squares '+str(clock())
	img5,sqHist5 = getSigSquares(aux,img.shape,(10,10),relevanceThresh)
	print '====>takes '+str(clock()-myTime)
	myTime = clock()


	#do backproyection for every non trivial entry in sqHist
	print 'backproyection '+str(clock())
	bpGeneral, bpComponent = bpSignificantSquares(img.copy(),sqHist5,probThresh)
	print '====>takes '+str(clock()-myTime)
	myTime = clock()

	print 'dilate '+str(clock())
	kernel = np.ones((3,3),np.uint8)*255
	bpComponentDilated = cv2.dilate(bpComponent.copy(),kernel,iterations=3,borderType=cv2.BORDER_CONSTANT,borderValue=0)
	#bpComponentDilated = cv2.erode(bpComponent.copy(),kernel,iterations=1,borderType=cv2.BORDER_CONSTANT,borderValue=0)
	print '====>takes '+str(clock()-myTime)

	blueShape = getBlueMask(img.copy(),cv2.split(bpComponentDilated)[0])

	
	print '====>takes '+str(clock()-myTime)
	myTime = clock()

	return blueShape





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
	

	histogram = [0,]*((img.shape[0]+2)*(img.shape[1]+2))

	f = open('parameters','r')
	parametersDict = pickle.load(f)
	f.close()

	imgParams = parametersDict[imageNames[imgIndex]]


	cv2.namedWindow('panel',cv2.cv.CV_WINDOW_NORMAL)
	cv2.namedWindow('ffP',cv2.cv.CV_WINDOW_NORMAL)
	#cv2.createTrackbar('thresh','panel',180,255,dummy)
	cv2.createTrackbar('probThresh','panel',1,256,dummy)
	cv2.createTrackbar('R','ffP',0,255,dummy2)
	cv2.createTrackbar('G','ffP',0,255,dummy2)
	cv2.createTrackbar('B','ffP',255,255,dummy2)
	cv2.createTrackbar('loDiff','ffP',1,255,dummy2)
	cv2.createTrackbar('upDiff','ffP',1,255,dummy2)

	

	changeParam = False

	blueShapeOriginal = doAndPack(img,imgParams['direction'],
		imgParams['thresh'],
		imgParams['canny'],
		imgParams['blat'],
		imgParams['relevanceThresh'],
		cv2.getTrackbarPos('probThresh','panel')
	)





	blueShapeCopy = blueShapeOriginal.copy()
	cv2.namedWindow('blueShape',cv2.cv.CV_WINDOW_NORMAL)
	blueShapeDim = (900,750)
	seedPoint = (0,0)
	changeSeed = False

	def onmouse(event, x, y, flags, param):
		global blueShapeCopy
		global seedPoint
		global changeSeed

		aux = (transform(x,y,img.shape,blueShapeDim))
		patch = cv2.pyrUp(cv2.getRectSubPix(blueShapeCopy, (100,100), aux))
		cv2.circle(patch,(100,100),2,(0,0,255),1)
		cv2.imshow('zoom',patch)

		if flags & (event == cv2.EVENT_FLAG_LBUTTON):
			seedPoint = aux
			changeSeed = True

	cv2.setMouseCallback('blueShape', onmouse)





	while True:
		

		if changeParam:
			imgParams = parametersDict[imageNames[imgIndex]]
			
			blueShapeOriginal = doAndPack(img,imgParams['direction'],
				imgParams['thresh'],
				imgParams['canny'],
				imgParams['blat'],
				imgParams['relevanceThresh'],
				cv2.getTrackbarPos('probThresh','panel')
			)

			blueShapeCopy = blueShapeOriginal.copy()
			changeParam = False


		if changeSeed:
			histogram = [0,]*((img.shape[0]+2)*(img.shape[1]+2))
			loDiff,upDiff = findBreakingPoint(blueShapeCopy,seedPoint)
			mask = np.zeros((blueShapeCopy.shape[0]+2,blueShapeCopy.shape[1]+2),np.uint8)
			newVal = (cv2.getTrackbarPos('B','ffP'),cv2.getTrackbarPos('G','ffP'),cv2.getTrackbarPos('R','ffP'))
			cv2.floodFill(blueShapeCopy, mask, seedPoint, newVal, loDiff, upDiff)
			changeSeed = False
			#fillHistogram(blueShapeCopy.copy(),seedPoint,histogram)
			#print histogram
			#for i in histogram:
			#	if histogram[i]>0:
			#		print str(histogram[i])+' elements with area '+str(i)
			print 'out of changeseed'

		#cv2.imshow('original',bigImg)
		cv2.imshow('blueShape',cv2.resize(blueShapeCopy,blueShapeDim))




		key = cv2.waitKey(5)
	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
	 		changeParam = True
	 		changeSeed = False
	 		histogram = [0,]*(img.shape[0]*img.shape[1])
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])
	 		changeParam = True
	 		changeSeed = False
	 		histogram = [0,]*((img.shape[0]+2)*(img.shape[1]+2))
	 	elif (key == 114):
	 		blueShapeCopy = blueShapeOriginal.copy()
	 	elif (key != -1):
	 		break









	
