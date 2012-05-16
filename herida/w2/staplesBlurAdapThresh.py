import cv2
import numpy as np
import sys
from glob import glob
import math


def dummy(x):
	print x


def blurAndAT(img,iterations,ksizeBlur,ksizeAT):
	iterations+=1
	ksizeBlur += 1
	ksizeAT = 2*ksizeAT+3

	bwImg = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)
	

	for i in range(iterations):
		bwImg = cv2.blur(bwImg,(ksizeBlur,ksizeBlur))
		bwImg = cv2.adaptiveThreshold(bwImg, 255,
			cv2.cv.CV_ADAPTIVE_THRESH_MEAN_C, 
			cv2.cv.CV_THRESH_BINARY, ksizeAT, 20)
	return bwImg


def findFrame(contours,canvas,axis):

	#compute the width and height of a square
	sqNum = 3
	lw = canvas.shape[1]/sqNum
	lh = canvas.shape[0]/sqNum

	
	if axis==0: #vertical frames	
		hist = [0,]*sqNum #create a histogram to store the info about the contours
		for cont in contours:
			center,r = cv2.minEnclosingCircle(cont) #we simplify computations.
			x = center[0]
			for i in range(sqNum):
				#if "center is in the frame"  or   the circle intersects the frame
				if(i*lw<x and (i+1)*lw>x) or (abs(x-i*lw)<r or abs(x-(i+1)*lw)<r):
					hist[i]+=1
		#paint the info stored in hist
		for i in enumerate(hist):
			if i[1]!=0:
				plane = np.ones((canvas.shape[0],lw),np.uint8)*125
				canvas[:,i[0]*lw:(i[0]+1)*lw,1]=plane	
	
	if axis==1: #horizontal frames	
		hist = [0,]*sqNum #create a histogram to store the info about the contours
		for cont in contours:
			center,r = cv2.minEnclosingCircle(cont) #we simplify computations.
			y = center[1]
			for i in range(sqNum):
				#if "center is in the frame"  or   the circle intersects the frame
				if(i*lh<y and (i+1)*lh>y)or(abs(y-i*lh)<r or abs(y-(i+1)*lh)<r):
					hist[i]+=1
		#paint the info stored in hist
		for i in enumerate(hist):
			if i[1]!=0:
				plane = np.ones((lh,canvas.shape[0]),np.uint8)*125
				canvas[i[0]*lh:(i[0]+1)*lh,:,1]=plane	
	
	if axis==2:#horizontal and vertical frames
		sqHist = [] #create an appropiate histogram (2D)
		for i in range(sqNum):
			aux = [0,]*sqNum
			sqHist.append(aux)

		for cont in contours:
			center,r = cv2.minEnclosingCircle(cont)
			x,y = center[0],center[1]
			for i in range(sqNum):
				#if "center is in the vertical frame"  or   the circle intersects the vertical frame
				if(i*lw<x and (i+1)*lw>x)or(abs(x-i*lw)<r or abs(x-(i+1)*lw)<r):
					for j in range(sqNum):
						#if "center is in the horizontal frame" or the circle intersects the horizontal frame
						if(j*lh<y and (j+1)*lh>y)or(abs(y-j*lh)<r or abs(y-(j+1)*lh)<r):
							sqHist[j][i]+=1
		#paint the result
		for row in enumerate(sqHist):
			for column in enumerate(row[1]):
				if column[1]!=0:
					plane = np.ones((lh,lw),np.uint8)*125
					canvas[row[0]*lh:(row[0]+1)*lh,column[0]*lw:(column[0]+1)*lw,1]=plane	


def stapleCont(img,minArea,maxArea,direction,frameIt):
	
	if minArea>maxArea:
		aux = maxArea
		maxArea = minArea
		minArea = aux

	h, w = img.shape[:2]
	canvas = np.zeros((h,w,3), np.uint8)

	rawContours,hierarchy = cv2.findContours(img.copy(),
		cv2.cv.CV_RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)

	bigCont = [] #contours with more than one element
	for cnt in rawContours:
		if len(cnt)>1:
			cvxH = cv2.convexHull(cnt)
			area = cv2.contourArea(cvxH,False)
			if (area>minArea and area<maxArea):
				bigCont.append(cvxH)
	
	lines =[]
	for points in enumerate(bigCont):
		l = cv2.fitLine(points[1], cv2.cv.CV_DIST_L2, 0, 0.1, 0.1)
		p = (l[2],l[3])
		v = (l[0],l[1])
		lines.append((points[0],v,p))

		
	directionHist = [0,0,0,0]	
	d0,d1,d2,d3 = [],[],[],[]
	contByDirection = [d0,d1,d2,d3]

	for vect in lines:
		
		index = vect[0]
		v = vect[1]
		p = vect[2]

		if math.degrees(math.asin(abs(v[1])))<45:
			if ((v[0]>0 and v[1]<=0) or (v[0]<0 and v[1]>=0)) :
				directionHist[0]+=1
				contByDirection[0].append(bigCont[vect[0]])
				if direction==0 or direction==4:
					p2 = (p[0]+10*v[0],p[1]+10*v[1])
					cv2.line(canvas,p,p2,(0,0,255),2)	
			else:
				directionHist[3]+=1
				contByDirection[3].append(bigCont[vect[0]])
				if direction==3 or direction==4:
					p2 = (p[0]+10*v[0],p[1]+10*v[1])
					cv2.line(canvas,p,p2,(0,0,255),2)
		else:
			if ((v[0]>=0 and v[1]<0) or (v[0]<=0 and v[1]>0)) :
				directionHist[1]+=1
				contByDirection[1].append(bigCont[vect[0]])
				if direction==1 or direction==4:
					p2 = (p[0]+10*v[0],p[1]+10*v[1])
					cv2.line(canvas,p,p2,(0,0,255),2)
			else:
				directionHist[2]+=1
				contByDirection[2].append(bigCont[vect[0]])
				if direction==2 or direction==4:
					p2 = (p[0]+10*v[0],p[1]+10*v[1])
					cv2.line(canvas,p,p2,(0,0,255),2)

	if direction == 5:
		cv2.drawContours(canvas,
			contByDirection[directionHist.index(max(directionHist))],
			-1, (255,255,255))
	else:
		cv2.drawContours(canvas, bigCont, -1, (255,255,255))
	
	findFrame(bigCont,canvas,2)

	return canvas #bigCont



def doAndPack(img,ksizeBlur,ksizeAT,minArea,maxArea,direction):
	
	h, w = 375,450
	blat = blurAndAT(img,2,ksizeBlur,ksizeAT)
	contoursCanvas = stapleCont(blat,minArea,maxArea,direction,1)
	
	background = np.zeros((h,w*3,3),np.uint8)
	background[0:h,0:w,0:3]=cv2.resize(img,(w,h))
	background[0:h,w:2*w,0]=cv2.resize(blat,(w,h))
	background[0:h,2*w:3*w,0:3]=cv2.resize(contoursCanvas,(w,h))
	return background




if __name__ == "__main__":


	path = '../images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])	
	
	cv2.namedWindow('panel',cv2.cv.CV_WINDOW_NORMAL)
	cv2.createTrackbar('ksizeBlur','panel',0,5,dummy)
	cv2.createTrackbar('ksizeAT','panel',0,4,dummy)
	cv2.createTrackbar('minArea','panel',0,500,dummy)
	cv2.createTrackbar('maxArea','panel',5000,5000,dummy)
	cv2.createTrackbar('direction','panel',0,5,dummy)

	bigImg = doAndPack(img,
		cv2.getTrackbarPos('ksizeBlur','panel'),
		cv2.getTrackbarPos('ksizeAT','panel'),
		cv2.getTrackbarPos('minArea','panel'),
		cv2.getTrackbarPos('maxArea','panel'),
		cv2.getTrackbarPos('direction','panel'))

	while True:

		bigImg = doAndPack(img,
		cv2.getTrackbarPos('ksizeBlur','panel'),
		cv2.getTrackbarPos('ksizeAT','panel'),
		cv2.getTrackbarPos('minArea','panel'),
		cv2.getTrackbarPos('maxArea','panel'),
		cv2.getTrackbarPos('direction','panel'))

		cv2.imshow('original',bigImg)
		
		
		key = cv2.waitKey(5)

	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])

	 	elif (key != -1):
	 		break









	
