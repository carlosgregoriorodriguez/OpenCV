#Very basic example of cornerHarris... only works for k = 0 and ksize = 1;
# ERROR with ksize = 5 ... why?
# TO QUIT press any key

import cv2
import numpy as np
import time

def dummy(x):
	print 2*x+1;
	return 2*x+1;

def dummy2(x):
	return x;

if __name__ == '__main__':

	print("To QUIT press any key");

	imgSTP = cv2.imread("../img/stop.jpg",0);  #0 for grayscale

	#create window and trackbars for apertureSize (kSize) of the Sobel and for k
	cv2.namedWindow("TBAR");
	cv2.createTrackbar("kSize","TBAR",0,3,dummy);  #must be either 1, 3, 5, or 7  ERROR at 5... only works at 1, others are black
	cv2.createTrackbar("k","TBAR",0,2,dummy2);

	while True:

		result = cv2.cornerHarris(imgSTP,blockSize=100,ksize=cv2.getTrackbarPos("kSize","TBAR"),k=cv2.getTrackbarPos("k","TBAR"));

		cv2.imshow("RESULT",result);

		if (cv2.waitKey(5)!=-1):
			break;

