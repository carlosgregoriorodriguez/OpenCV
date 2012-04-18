
import cv2
import cv2.cv as cv
import numpy as np
import time

def dummy(x):
	print 2*x+1;
	return 2*x+1;

def dummy2(x):
	pass; #return x;

if __name__ == '__main__':

	img = cv2.imread("../img/stop.jpg",0);  #0 for grayscale

	cv2.imshow("ORIGINAL",img);

	#create trackbar window
	cv2.namedWindow("Trackbars");

	#create trackbars
	cv2.createTrackbar("dp","Trackbars",1,2,dummy2);
	cv2.createTrackbar("minDist","Trackbars",2,100,dummy);
	cv2.createTrackbar("minRadius","Trackbars",0,50,dummy);  #OPTIONAL
	cv2.createTrackbar("maxRadius","Trackbars",0,200,dummy); #OPTIONAL


	mthd = cv.CV_HOUGH_GRADIENT   #only method implemented for HoughCircles, CV_HOUGH_GRADIENT = 3

	while True:

		#if the OPTIONAL trackbars are at 0
		if cv2.getTrackbarPos("minRadius","Trackbars")==0 or cv2.getTrackbarPos("maxRadius","Trackbars")==0: #if the trackbars are at 0
			result = cv2.HoughCircles(img,method=mthd,
				dp=cv2.getTrackbarPos("dp","Trackbars"),minDist=cv2.getTrackbarPos("minDist","Trackbars"));

		else :
			result = cv2.HoughCircles(img,method=mthd,dp=cv2.getTrackbarPos("dp","Trackbars"),
				minDist=cv2.getTrackbarPos("minDist","Trackbars"),minRadius=cv2.getTrackbarPos("minRadius","Trackbars"),
				maxRadius=cv2.getTrackbarPos("maxRadius","Trackbars"));

		#print(result);

		if (cv2.waitKey(5)!=-1):
			break

	print(result);






		



