import cv2
import numpy as np
import sys
from glob import glob
import math


def dummy(x):
	print x


#Methods for finding up staples in a 3-channel image

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


def thresholdChannels(img):
	mergeAux=[]
	for channel in cv2.split(img):
		mergeAux.append(cv2.threshold(channel,180,255,cv2.cv.CV_THRESH_BINARY)[1])
	
	aux = cv2.min(mergeAux[0],mergeAux[1])
	aux = cv2.min(aux,mergeAux[2])
	return cv2.merge([aux]*3)



#Methods for treating the staple contours
def findFrame(contours,dimension,axis,val,sqNum):
	#compute the width and height of a square
	lw = dimension[0]/sqNum
	lh = dimension[1]/sqNum
	
	if axis==2:#horizontal and vertical frames
		sqHist = np.zeros((sqNum,)*2,np.uint8) #create an appropiate histogram (2D)
		for cont in contours:	#for every contour, we update the histogram
			center,r = cv2.minEnclosingCircle(cont) #take the minimal enclosing circle for the contour
			x,y = center[0],center[1]
			for row in range(sqNum):
				#if "center is in the horizontal frame" or the circle intersects the horizontal frame
				if(row*lh<y and (row+1)*lh>y)or(abs(y-row*lh)<r or abs(y-(row+1)*lh)<r):
					for col in range(sqNum):
						#if "center is in the vertical frame"  or   the circle intersects the vertical frame
						if(col*lw<x and (col+1)*lw>x)or(abs(x-col*lw)<r or abs(x-(col+1)*lw)<r):
							sqHist[row,col]+=1	
		return sqHist


def stapleCont(img,minArea,maxArea,direction):	
	if minArea>maxArea:
		minArea,maxArea=maxArea,minArea

	canvas = np.zeros((img.shape), np.uint8)

	rawContours,hierarchy = cv2.findContours(img.copy(),
		cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

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

		
	directionHist = [0,]*4	
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

	return canvas,bigCont


def stapleContThresh(img,minArea,maxArea,direction):
	threshChan = thresholdChannels(img)
	c1,c2,c3 = cv2.split(threshChan)
	aux = cv2.max(c1,c2)
	aux = cv2.max(aux,c3)
	return stapleCont(aux,minArea,maxArea,direction)


def paintSQS(sqHist,img):
	totalH,totalW = img.shape[:2]
	rowNum,colNum = sqHist.shape[:2]

	canvas = np.zeros((totalH,totalW),np.uint8)
	lw = totalW/colNum
	lh = totalH/rowNum
	#paint the result
	for row in range(rowNum-1):
		for col in range(colNum-1):
			print sqHist.shape
			print [row,rowNum-1]
			print [col,colNum-1]
			if sqHist[row][col]!=0:
				plane = np.ones((lh,lw),np.uint8)*255
				canvas[row*lh:(row+1)*lh,col*lw:(col+1)*lw]=plane	
	
	return cv2.merge([cv2.min(canvas,layer) for layer in cv2.split(img)])


def isConnected(row,col,matrix):
	leftB = max(0,col-1)
	rightB = min(col+1,matrix.shape[1]-1)
	upB = max(0,row-1)
	downB = min(row+1,matrix.shape[0]-1)
	for i in range(upB,downB+1,1):
		for j in range(leftB,rightB+1,1):
			if (i!=row or j!=col) and (matrix[i,j]!=0):
				return True
	return False


def removeNotConnected(sigSquares):
	for row in range(sigSquares.shape[0]-1):
		for col in range(sigSquares.shape[1]-1):
			if (sigSquares[row,col]!=0) and (not isConnected(row,col,sigSquares)):
				sigSquares[row,col]=0


def refine(sigSquares,img,bigCont,minArea,maxArea,direction,refDim):
	lh,lw=img.shape[0]/sigSquares.shape[0],img.shape[1]/sigSquares.shape[1]
	mask = np.zeros((img.shape),np.uint8)
	refSquares = np.zeros((len(sigSquares)*refDim[1],len(sigSquares[0])*refDim[0]),np.uint8)
	for row in range(sigSquares.shape[0]-1):
		for col in range(sigSquares.shape[1]-1):
			#if the square value is greater than 0 (i.e there is a contour in this tile)
			#then we get the sigSquares of this particular tile
			if sigSquares[row,col]!=0:
				patch = img[row*lh:(row+1)*lh,col*lw:(col+1)*lw,:]
				patchCont = stapleContThresh(patch,minArea,maxArea,direction)[1]
				patchSquares = findFrame(patchCont,(lw,lh),2,255,5)
				removeNotConnected(patchSquares)
				refSquares[row*refDim[1]:(row+1)*refDim[1],col*refDim[0]:(col+1)*refDim[0]]=patchSquares
	return refSquares
#removeNotConnected(refSquares)


def significantSQS(img,bigCont,minArea,maxArea,direction):
	sigSquares = findFrame(bigCont,(img.shape[1],img.shape[0]),2,255,5)
	print type(sigSquares)
	removeNotConnected(sigSquares)
	sigSquares = refine(sigSquares,img,bigCont,minArea,maxArea,direction,(5,5))
	print type(sigSquares)
	aux = paintSQS(sigSquares,np.ones((img.shape),np.uint8)*255)
	rawContours,hierarchy = cv2.findContours(cv2.split(aux)[0].copy(),
		cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	convex = [cv2.convexHull(points) for points in rawContours]
	cv2.drawContours(img,convex,-1, (0,0,255),3)
	
	return img
	

def doAndPack(img,minArea,maxArea,direction):
	h, w = 375,450

	threshChan,bigCont = stapleContThresh(img,minArea,maxArea,direction)
	copyImg = significantSQS(img,bigCont,minArea,maxArea,direction)

	background = np.zeros((h,w*3,3),np.uint8)
	background[0:h,0:w,0:3]=cv2.resize(img,(w,h))
	background[0:h,w:2*w,0:3]=cv2.resize(cv2.merge([threshChan,]*3),(w,h))
	background[0:h,2*w:3*w,0:3]=cv2.resize(copyImg,(w,h))
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
	cv2.createTrackbar('minArea','panel',0,500,dummy)
	cv2.createTrackbar('maxArea','panel',5000,5000,dummy)
	cv2.createTrackbar('direction','panel',0,5,dummy)

	bigImg = doAndPack(img,
		cv2.getTrackbarPos('minArea','panel'),
		cv2.getTrackbarPos('maxArea','panel'),
		cv2.getTrackbarPos('direction','panel'))

	while True:

		bigImg = doAndPack(img,
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









	
