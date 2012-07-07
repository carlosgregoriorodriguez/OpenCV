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

def dummy(x):
	global changeParam
	changeParam = True
	print x


def doAndPack(img,dirList,thresh,cannyList,blatList,relevanceThresh,probThresh,winDim):
	print 'NEW IMAGE'
	print 'current time: '+str(clock())

	h = winDim[1]
	w = winDim[0]
	border = 20
	
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

	img5 = cv2.merge([cv2.min(img5,layer) for layer in cv2.split(backEqImg)])

	#do backproyection for every non trivial entry in sqHist
	print 'backproyection '+str(clock())
	bpGeneral, bpComponent = bpSignificantSquares(img.copy(),sqHist5,probThresh)
	print '====>takes '+str(clock()-myTime)
	myTime = clock()

	print 'dilate '+str(clock())
	kernel = np.ones((3,3),np.uint8)*255
	bpComponentDilated = cv2.dilate(bpComponent.copy(),kernel,iterations=3,borderType=cv2.BORDER_CONSTANT,borderValue=0)
	print '====>takes '+str(clock()-myTime)

	print 'build the canvas'
	background = np.zeros((h*2+2*border,w*3,3),np.uint8)
	background[border:h+border,0:w,0:3]=cv2.resize(img,(w,h))
	background[border:h+border,w:2*w,0:3]=cv2.resize(backEqImg,(w,h))
	background[border:h+border,2*w:3*w,0:3]=cv2.resize(img5,(w,h))

	background[h+2*border:2*h+2*border,0:w,0:3]=cv2.resize(bpComponentDilated,(w,h))
	background[h+2*border:2*h+2*border,w:2*w,0:3]=cv2.resize(cv2.min(img,bpComponentDilated),(w,h))
	
	cv2.putText(background, 'original RGB', (0,border-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
	cv2.putText(background, 'HSV + histograma ecualizado', (w,border-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
	cv2.putText(background, 'localizacion de las grapas', (2*w,border-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
	
	cv2.putText(background, 'mascara de back projection', (0,h+2*border-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
	cv2.putText(background, 'zona de piel recortada', (w,h+2*border-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
	
	print '====>takes '+str(clock()-myTime)
	myTime = clock()

	return background



def backproyectionMethod(imgIndex,imageNames,parameterDict):
	global changeParam

	img = cv2.imread(imageNames[imgIndex])
	imgParameters = parameterDict[imageNames[imgIndex]]
	
	dirList = imgParameters['direction']
	blatList = imgParameters['blat'] 
	cannyList =imgParameters['canny']
	thresh = imgParameters['thresh']
	relevanceThresh = imgParameters['relevanceThresh']
	
	cv2.namedWindow('backproyection',cv2.cv.CV_WINDOW_NORMAL)
	cv2.createTrackbar('probabilityThresh','backproyection',5,20,dummy)
	probThresh = cv2.getTrackbarPos('probabilityThresh','backproyection')

	cv2.namedWindow('panel window size',cv2.cv.CV_WINDOW_NORMAL)
	cv2.createTrackbar('width','panel window size',450,1500,dummy)
	cv2.createTrackbar('height','panel window size',375,1500,dummy)
	winDim = (cv2.getTrackbarPos('width','panel window size'),cv2.getTrackbarPos('height','panel window size'))


	background = doAndPack(img,dirList,thresh,cannyList,blatList,relevanceThresh,probThresh,winDim)
	
	changeParam = False
	changeImg = False
	edit = False
	while True:
		if changeImg:	
			imgParameters = parameterDict[imageNames[imgIndex]]

			dirList = imgParameters['direction']
			blatList = imgParameters['blat'] 
			cannyList =imgParameters['canny']
			thresh = imgParameters['thresh']
			relevanceThresh = imgParameters['relevanceThresh']
			probThresh = cv2.getTrackbarPos('probabilityThresh','backproyection')
			winDim = (cv2.getTrackbarPos('width','panel window size'),cv2.getTrackbarPos('height','panel window size'))

			background = doAndPack(img,dirList,thresh,cannyList,blatList,relevanceThresh,probThresh,winDim)

			changeImg=False

		if changeParam and edit:
			dirList = [cv2.getTrackbarPos('minArea','panel direction'),
				cv2.getTrackbarPos('maxArea','panel direction'),
				cv2.getTrackbarPos('direction','panel direction')]
		
			cannyList = [cv2.getTrackbarPos('canny thresh1','panel canny'),
				cv2.getTrackbarPos('canny thresh2','panel canny')]

			blatList = [cv2.getTrackbarPos('iterations','panel blur+adapt threshold'),
				(cv2.getTrackbarPos('ksizeBlur X','panel blur+adapt threshold'),cv2.getTrackbarPos('ksizeBlur Y','panel blur+adapt threshold')),
				cv2.getTrackbarPos('ksizeAT','panel blur+adapt threshold')]

			thresh = cv2.getTrackbarPos('thresh','panel findStaples')
			relevanceThresh = cv2.getTrackbarPos('relevanceThresh','panel findStaples')
			probThresh = cv2.getTrackbarPos('probabilityThresh','backproyection')

			winDim = (cv2.getTrackbarPos('width','panel window size'),cv2.getTrackbarPos('height','panel window size'))
			background = doAndPack(img,dirList,thresh,cannyList,blatList,relevanceThresh,probThresh,winDim)
			
			changeParam = False
		elif changeParam:
			probThresh = cv2.getTrackbarPos('probabilityThresh','backproyection')
			winDim = (cv2.getTrackbarPos('width','panel window size'),cv2.getTrackbarPos('height','panel window size'))
			background = doAndPack(img,dirList,thresh,cannyList,blatList,relevanceThresh,probThresh,winDim)
			changeParam = False

		cv2.imshow('backproyected image',background)
		
		key = cv2.waitKey(5)
		if (key==120):#x to move to the right
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
	 		changeImg = True
	 	elif (key==122):#z to move to the left
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])
	 		changeImg = True
		elif (key==101):#e to enter or exit edit mode
			if not edit:
				cv2.namedWindow('panel findStaples',cv2.cv.CV_WINDOW_NORMAL)
				cv2.namedWindow('panel canny',cv2.cv.CV_WINDOW_NORMAL)
				cv2.namedWindow('panel blur+adapt threshold',cv2.cv.CV_WINDOW_NORMAL)
				cv2.namedWindow('panel direction',cv2.cv.CV_WINDOW_NORMAL)
				cv2.createTrackbar('minArea','panel direction',5,500,dummy)
				cv2.createTrackbar('maxArea','panel direction',5000,5000,dummy)
				cv2.createTrackbar('direction','panel direction',5,5,dummy)
				cv2.createTrackbar('canny thresh1','panel canny',500,700,dummy)
				cv2.createTrackbar('canny thresh2','panel canny',700,700,dummy)
				cv2.createTrackbar('iterations','panel blur+adapt threshold',1,10,dummy)
				cv2.createTrackbar('ksizeBlur X','panel blur+adapt threshold',3,4,dummy)
				cv2.createTrackbar('ksizeBlur Y','panel blur+adapt threshold',3,4,dummy)
				cv2.createTrackbar('ksizeAT','panel blur+adapt threshold',2,4,dummy)
				cv2.createTrackbar('relevanceThresh','panel findStaples',2,3,dummy)
				cv2.createTrackbar('thresh','panel findStaples',180,255,dummy)
				edit = True
			else:
				cv2.destroyWindow('panel findStaples')
				cv2.destroyWindow('panel canny')
				cv2.destroyWindow('panel blur+adapt threshold')
				cv2.destroyWindow('panel direction')

				imgParameters = parameterDict[imageNames[imgIndex]]
				dirList = imgParameters['direction']
				blatList = imgParameters['blat'] 
				cannyList =imgParameters['canny']
				thresh = imgParameters['thresh']
				relevanceThresh = imgParameters['relevanceThresh']
				
				edit = False
				changeParam = False
				changeImg = True

		elif (key == 115):#s to save the selected parameters
			parameter = {'direction':dirList , 'blat':blatList ,
	 		 'canny':cannyList , 'thresh':thresh,
	 		 'relevanceThresh':relevanceThresh,
	 		 'probThresh':probThresh}
	 		parameterDict[imageNames[imgIndex]]=parameter
			f = open('parameters','w')
	 		pickle.dump(parameterDict,f)
	 		f.close()


		elif (key==113):#q to exit
	 		cv2.destroyWindow('panel findStaples')
			cv2.destroyWindow('panel canny')
			cv2.destroyWindow('panel blur+adapt threshold')
			cv2.destroyWindow('panel direction')
			cv2.destroyWindow('backproyection')
	 		cv2.destroyWindow('backproyected image')
	 		cv2.destroyWindow('panel window size')

	 		break




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
	
	f = open('parameters','r')
	parameterDict = pickle.load(f)
	f.close()

	backproyectionMethod(imgIndex,imageNames,parameterDict)

	
