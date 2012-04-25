import cv2
import numpy as np
import math


def dummy(x):
	print x



if __name__ == "__main__":

	original = cv2.imread('../../img/lines.jpg')
	image = cv2.cvtColor(original,cv2.cv.CV_RGB2GRAY)


	cv2.namedWindow('panel',cv2.cv.CV_WINDOW_NORMAL)
	cv2.createTrackbar('rho','panel',5,500,dummy)
	cv2.createTrackbar('theta','panel',1,90,dummy)
	cv2.createTrackbar('threshold','panel',1,900,dummy)
	cv2.createTrackbar('minDist','panel',40,100,dummy)

	theta = math.radians(40)
	while True:

		#theta = math.radians(cv2.getTrackbarPos('theta','panel'))
		rho = cv2.getTrackbarPos('rho','panel')
		threshold = cv2.getTrackbarPos('threshold','panel')

		lines = cv2.HoughLinesP(image, rho, theta, threshold)
		
		minDist = cv2.getTrackbarPos('minDist','panel')
		for line in lines[0]:
			pA = (line[0],line[1])
			pB = (line[2],line[3])
			#if (math.sqrt(abs(pA[0]-pB[0])**2+abs(pA[1]-pB[1])**2)>minDist):
			cv2.line(original,pA,pB,(0,255,0),2)

		
		cv2.imshow('lines',original)
		
		key = cv2.waitKey(5)

	 	if (key != -1):
	 		break









	