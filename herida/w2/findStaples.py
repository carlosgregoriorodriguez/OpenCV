import cv2
import numpy as np
import sys
from glob import glob
import math


def dummy(x):
	print x


def ffCenter(img,mask):
	y = img.shape[0]
	x = img.shape[1]
	seeds = []
	for px in range(int(x/3),int(2*x/3)+1,int(x/3)):
		for py in range(int(y/3),int(2*y/3)+1,int(y/3)):
			seeds.append((px,py))
	lo = 5
	hi = 5
	for seed in seeds:
		cv2.floodFill(img, mask, seed, (255, 255, 255), (lo,)*3, (hi,)*3)
	img = cv2.threshold(img, 200, 0, cv2.THRESH_TOZERO)[1]
	return img


def fleshContours(img):
	h, w = img.shape[:2]
	canvas = np.zeros((h,w), np.uint8)
	rawContours,hierarchy = cv2.findContours(img.copy(),
		cv2.cv.CV_RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)
	contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in rawContours]
	center = (img.shape[1]/2,img.shape[0]/2)
	selectedCnts = []
	for cnt in contours:
		if (cv2.contourArea(cnt,False)>=(img.shape[0]/3)*(img.shape[1]/3) 
			and cv2.pointPolygonTest(cnt,center,False)>0):
			selectedCnts.append(cnt)
	cv2.drawContours(canvas,selectedCnts,-1,(255,255,255),cv2.cv.CV_FILLED)
	return canvas


def cutImage(img,mask):
	channels = []
	for channel in cv2.split(img):
		channels.append(cv2.max(channel,mask))
	return cv2.merge(channels)


def fitContours(smallCont,bigCont):
	if len(smallCont)>0 and len(bigCont)>0:
		rectangles = []
		r = 0
		center = (0,0)
		for bigC in enumerate(bigCont):
			mar = cv2.minAreaRect(bigC[1])
			rectangles.append((bigC[0],mar))
			print mar
		sorted(rectangles, key=lambda circle:circle[2])
		
		for smallElem in smallCont:
			x = smallElem[0][0][0]
			y = smallElem[0][0][1]
			for circle in cntCircles:
				if math.sqrt(math.pow(abs(x-circle[1][0]),2)+math.pow(abs(y-circle[1][1]),2))<2*circle[2]:
					newCont = np.append(smallElem,circle[0], axis=0)
					fittedPoints.append(smallElem)
	

def fitWithLine(smallCont,lines,bigCont):
	for sC in smallCont:
		for line in lines:
			if distace(sC,line[1])<TOL:
				np.append(sC,bigCont[line[0]])
				break
	

def stapleCont(img):
	h, w = img.shape[:2]
	canvas = np.zeros((h,w), np.uint8)

	rawContours,hierarchy = cv2.findContours(img.copy(),
		cv2.cv.CV_RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)

	"""we divide the contours in two different groups.
		The contours with more than one element, and the others
	"""
	bigCont = [] #contours with more than one element
	smallCont = [] #contours with exactly one element
	for cnt in rawContours:
		if len(cnt)>1:
			print cnt
		poly = cv2.approxPolyDP(cnt, 3, True)
		if len(poly)>1:
			bigCont.append(poly)
		else:
			smallCont.append(poly)

	#for each one-element contour we try to fit it into a bigger contour.
	fitContours(smallCont,bigCont)

	lines = []
	for points in enumerate(bigCont):
		if len(points[1])>1:
			l = cv2.fitLine(points[1], cv2.cv.CV_DIST_L2, 0, 0.1, 0.1)
			p = (l[2],l[3])
			p2 = (p[0]+l[0],p[1]+l[1])
			lines.append((points[0],(p,p2))
			cv2.line(canvas,p,p2,(255,255,255))

	fitWithLine(smallCont,lines,bigCont)

	#echar un vistazo a minAreaRect y a fitLine
	return canvas




def doAndPack(img,thresh1,thresh2):
	hueImg = cv2.split(cv2.cvtColor(img, cv2.cv.CV_BGR2HSV))[0]
	h, w = img.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	ffImg = ffCenter(hueImg.copy(),mask)

	canvasInv = cv2.threshold(fleshContours(ffImg), 100, 255, cv2.THRESH_BINARY_INV)[1]
	cuttedImg = cutImage(img,canvasInv)

	cannyImg = cv2.Canny(cv2.cvtColor(cuttedImg,cv2.cv.CV_RGB2GRAY), thresh1, thresh2)
	
	contoursCanvas = stapleCont(cannyImg)

	background = np.zeros((h,w*3),np.uint8)
	background[0:h,0:w]=cv2.cvtColor(cuttedImg,cv2.cv.CV_RGB2GRAY)
	background[0:h,w:2*w]=cannyImg
	background[0:h,2*w:3*w]=contoursCanvas
	return background




if __name__ == "__main__":


	path = 'images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])	
	
 
	cv2.namedWindow('panel',cv2.cv.CV_WINDOW_NORMAL)
	cv2.createTrackbar('canny thresh1','panel',1500,1500,dummy)
	


	bigImg = doAndPack(img,
		cv2.getTrackbarPos('canny thresh1','panel'),
		cv2.getTrackbarPos('canny thresh1','panel'))


	while True:

		bigImg = doAndPack(img,
			cv2.getTrackbarPos('canny thresh1','panel'),
			cv2.getTrackbarPos('canny thresh1','panel'))

		cv2.imshow('original + hue Channel + ff',bigImg)
		
		
		key = cv2.waitKey(5)

	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])

	 	elif (key != -1):
	 		break









	
