import cv2
import numpy as np
import sys
from glob import glob



def dummy(x):
	print x

def getHist (img):
	hist_item = cv2.calcHist(img,[0],None,[180],[0,180])
	return hist_item

def getCentralRect(img):
	y = img.shape[0]
	x = img.shape[1]

	center = (int(x/2),int(y/2))
	patchSize = (int(x/3),int(y/3))
	return cv2.getRectSubPix(img, patchSize, center)


if __name__ == "__main__":


	mask = 'images/*.jpg'
	imageNames = glob(mask)

	img1 = cv2.imread(imageNames[4])	
	hsv1 = cv2.cvtColor(img1, cv2.cv.CV_BGR2HSV)
	hueImg = cv2.split(hsv1)[0]
	histHue1 = getHist(hueImg)

	centerSubRect = getCentralRect(hueImg)
	subRectHist = getHist(centerSubRect)
	null,maxSubRect,null,locSR= cv2.minMaxLoc(subRectHist)
	print "maxHue1: "+str(maxSubRect)+" at "+str(locSR)
	x = locSR[1]

	cv2.namedWindow("panel",cv2.cv.CV_WINDOW_NORMAL)
	cv2.createTrackbar("minus","panel",0,x,dummy)
	cv2.createTrackbar("plus","panel",0,255-x,dummy)

	while True:

		minus = cv2.getTrackbarPos("minus","panel")
		plus = cv2.getTrackbarPos("plus","panel")
		
		hueImgT1 = cv2.threshold(hueImg, x-minus, 0, cv2.THRESH_TOZERO)[1]

		hueImgT2 = cv2.threshold(hueImgT1, x+plus, 0, cv2.THRESH_TOZERO_INV)[1]

		hueImgT3 = cv2.threshold(hueImgT2, 2, 255 ,cv2.THRESH_BINARY)[1]

		cv2.imshow("original",img1)
		cv2.imshow("hueImg",hueImg)
		cv2.imshow("c",centerSubRect)
		cv2.imshow("hueImgT1",hueImgT1)
		cv2.imshow("hueImgT2",hueImgT2)
		cv2.imshow("hueImgT3",hueImgT3)
	
		
	 	if (cv2.waitKey(5)!=-1):
	 		break









	