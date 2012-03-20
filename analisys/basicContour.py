import cv2
import numpy as np
import sys



def dummy(x):
	print x

if __name__ == "__main__":

	# img is obtained as follows: load image -> converted to gray -> threshold binary(threshold = 128, maxval = 255)
	img = cv2.threshold(cv2.cvtColor(cv2.imread('../img/fields.jpg'),cv2.cv.CV_RGB2GRAY), 128, 255, cv2.THRESH_BINARY)[1]

	# a black canvas of the size of the image to draw the contours
	canvas = np.zeros((img.shape[0],img.shape[1]),np.uint8)


	#create a window
	cv2.namedWindow("contour")
    
	#create a trackbar that controlls the mode argument of the function findContours
	cv2.createTrackbar("mode","contour",0,3,dummy)

	# dictionary with the four constants for mode
	modeDict = {0:cv2.cv.CV_RETR_EXTERNAL,
		1:cv2.cv.CV_RETR_LIST ,
		2:cv2.cv.CV_RETR_CCOMP ,
		3:cv2.cv.CV_RETR_TREE}


	#create a trackbar to select contours with bigger or equal area than this trackbar position
	#if the trackbar is at maximum, then all the contours are shown (should be like trackbar at 0)
	trackbarMax=500
	cv2.createTrackbar("contour Area","contour",10,trackbarMax,dummy)


	while True:		
		rawContours,hierarchy = cv2.findContours(img.copy(),
			modeDict[cv2.getTrackbarPos("mode","contour")],
			cv2.CHAIN_APPROX_SIMPLE)

		aux = canvas.copy()
		
		# replace contours with approxPolyDP (it's nice)
		contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in rawContours]


		#if the trackbar is not the maximum value
		if cv2.getTrackbarPos("contour Area","contour")==trackbarMax:
			cv2.drawContours(aux,contours,-1,(255,255,255))

		#else
		else:
			bigContours = [cnt if cv2.contourArea(cnt)>cv2.getTrackbarPos("contour Area","contour") else None for cnt in contours ]
			cv2.drawContours(aux,bigContours,-1,(255,255,255))



		cv2.imshow("passed img transformed",img)
		cv2.imshow("contour",aux)

		
		if (cv2.waitKey(5)!=-1):
			break

















