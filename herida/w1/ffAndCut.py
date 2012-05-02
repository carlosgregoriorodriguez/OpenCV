import cv2
import numpy as np
import sys
from glob import glob



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


def contours(img):
	print 'enters in contours'
	h, w = img.shape[:2]
	canvas = np.zeros((h,w), np.uint8)
	rawContours,hierarchy = cv2.findContours(img.copy(),
		cv2.cv.CV_RETR_LIST,
		cv2.CHAIN_APPROX_SIMPLE)
	contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in rawContours]
	print 'contours l: '+str(len(contours))
	center = (img.shape[1]/2,img.shape[0]/2)
	selectedCnts = []
	for cnt in contours:
		if (cv2.contourArea(cnt,False)>=(img.shape[0]/3)*(img.shape[1]/3) 
			and cv2.pointPolygonTest(cnt,center,False)>0):
			selectedCnts.append(cnt)
	print len(selectedCnts)
	cv2.drawContours(canvas,selectedCnts,-1,(255,255,255),cv2.cv.CV_FILLED)
	return selectedCnts[0],canvas


def cutImage(img,mask):
	channels = []
	for channel in cv2.split(img):
		channels.append(cv2.max(channel,mask))
	return cv2.merge(channels)

def doAndPack(img):
	hueImg = cv2.split(cv2.cvtColor(img, cv2.cv.CV_BGR2HSV))[0]
	h, w = img.shape[:2]
	mask = np.zeros((h+2, w+2), np.uint8)
	ffImg = ffCenter(hueImg.copy(),mask)

	contour = []
	canvas = np.zeros((h,w), np.uint8)
	contour,canvas = contours(ffImg)
	canvasInv = cv2.threshold(canvas, 100, 255, cv2.THRESH_BINARY_INV)[1]
	
	cuttedImg = cutImage(img,canvasInv)
	
	background = np.zeros((h*2,w*3),np.uint8)
	background[0:h,0:w]=cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)
	background[0:h,w:2*w]=hueImg
	background[0:h,2*w:3*w]=ffImg
	background[h:2*h,0:w]=canvas
	background[h:2*h,w:2*w]=cv2.cvtColor(cuttedImg,cv2.cv.CV_RGB2GRAY)
	
	return background


if __name__ == "__main__":


	path = '../images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])	
	

	bigImg = doAndPack(img)
	
	def changeImg(imgName):
		newImg = cv2.imread(imgName)
		return doAndPack(newImg)

	while True:

		cv2.imshow('original + hue Channel + ff',bigImg)
		
		
		key = cv2.waitKey(5)

	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		bigImg = changeImg(imageNames[imgIndex])
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		bigImg = changeImg(imageNames[imgIndex])

	 	elif (key != -1):
	 		break









	
