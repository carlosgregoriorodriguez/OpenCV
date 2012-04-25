
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

	imgAUX = cv2.imread("../img/stop.jpg",0);  #0 for grayscale

	#apply GaussianBlur to smoothen image (reduces the number of false circles detected)
	img = cv2.GaussianBlur(imgAUX, ksize = (3,3), sigma1= 0);

	#cv2.imshow("GaussianBlur",img)

	#create trackbar window
	cv2.namedWindow("Trackbars");

	#create trackbars
	cv2.createTrackbar("dp","Trackbars",1,2,dummy2);
	cv2.createTrackbar("minDist","Trackbars",2,400,dummy);
	cv2.createTrackbar("minRadius","Trackbars",0,200,dummy);  #OPTIONAL
	cv2.createTrackbar("maxRadius","Trackbars",50,400,dummy); #OPTIONAL


	mthd = cv.CV_HOUGH_GRADIENT   #only method implemented for HoughCircles, CV_HOUGH_GRADIENT = 3

	while True:

		hghcrcl = [];
		hghcrcl = cv2.HoughCircles(img,method=mthd,dp=cv2.getTrackbarPos("dp","Trackbars"),
			minDist=cv2.getTrackbarPos("minDist","Trackbars"));

		#if the OPTIONAL trackbars are at 0
		# if cv2.getTrackbarPos("minRadius","Trackbars")==0 or cv2.getTrackbarPos("maxRadius","Trackbars")==0: #if the trackbars are at 0
		# 	result = cv2.HoughCircles(img,method=mthd,
		# 		dp=cv2.getTrackbarPos("dp","Trackbars"),minDist=cv2.getTrackbarPos("minDist","Trackbars"));

		# else :
		# 	result = cv2.HoughCircles(img,method=mthd,dp=cv2.getTrackbarPos("dp","Trackbars"),
		# 		minDist=cv2.getTrackbarPos("minDist","Trackbars"),minRadius=cv2.getTrackbarPos("minRadius","Trackbars"),
		# 		maxRadius=cv2.getTrackbarPos("maxRadius","Trackbars"));

		print(hghcrcl);
		hghcrcl = hghcrcl[0];
		
		for circle in hghcrcl:
			posX = circle[0];
			posY = circle[1];
			radius = circle[2];
			cv2.circle(img, (posX, posY), radius, (255, 0, 0));

		cv2.imshow("HoughCircles",img);

		if (cv2.waitKey(5)!=-1):
			break

	print(result);






		



