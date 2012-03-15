#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import numpy as np


def getPolishedHist(img):
	img = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)

	hist_item = cv2.calcHist([img],[0],None,[256],[0,255]) 
		
	cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
		
	return hist_item
	
def dummy(v):
	print "value "+str(v)
     

if __name__ == "__main__":

	print "Compares histograms of two captures of the webcam"
	print "move the trackbar to change the distance used to compare histograms"
	print ""
	print "press 'r' to capture a new frame for the firts histogram"
	print "press 'h' to capture a new frame for the second histogram"
	print "press 'Esc' to exit"


	camera = cv2.VideoCapture(0)


	# creates the window where the captures will be displayed
	# and the trackbar for the different distances
	cv2.namedWindow("captures")


	cv2.createTrackbar("Distance type","captures",0,3,dummy)

	d = {0:(cv2.cv.CV_COMP_CORREL,"CORREL"),
		1:(cv2.cv.CV_COMP_CHISQR,"CHISQR"),
		2:(cv2.cv.CV_COMP_INTERSECT,"INTERSECT"),
		3:(cv2.cv.CV_COMP_BHATTACHARYYA,"BHATTACHARYYA")}



	# initialices the first histogram
	f,img = camera.read()
	
	firstHist=getPolishedHist(img)



	# creates the big image where both captures are copied
	upBorder = 40

	blackBorder = np.zeros((upBorder,img.shape[1]*2,img.shape[2]),np.uint8)

	bigImg = np.zeros((img.shape[0]+upBorder,img.shape[1]*2,img.shape[2]),np.uint8)

	bigImg[upBorder:img.shape[0]+upBorder,0:img.shape[1]]=img
	
	cv2.imshow("captures",bigImg)


	


	while True:

		f,img = camera.read()
		
		cv2.imshow("webcam",img)

		key = cv2.waitKey(5)

		
		
		#114 --> r
		if (key == 114):

			# the first histogram and the first captureis are actualized 

			firstHist = getPolishedHist(img)

			bigImg[upBorder:img.shape[0]+upBorder,0:img.shape[1],:]=img

			cv2.imshow("captures",bigImg)


		#104 --> h
		if (key == 104):

			# the second histogram and second capture are actualized and the comparison is shown

			actualHist=getPolishedHist(img)

			distHist = cv2.compareHist(firstHist,actualHist,d[cv2.getTrackbarPos("Distance type","captures")][0])

			bigImg[0:upBorder,0:bigImg.shape[1],:]=blackBorder

			cv2.putText(bigImg,d[cv2.getTrackbarPos("Distance type","captures")][1]+" "+str(distHist),(upBorder,upBorder),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))

			bigImg[upBorder:img.shape[0]+upBorder,img.shape[1]:bigImg.shape[1],:]=img

			cv2.imshow("captures",bigImg)


		#27 --> esc
		if (key == 27):
			break

