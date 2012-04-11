import cv2
import numpy as np
import sys



def dummy(x):
	print x


if __name__ == "__main__":


	print """
		Trackbar mode: 	0 -> CV_RETR_EXTERNAL
						1 -> CV_RETR_LIST
						2 -> CV_RETR_CCOMP
						3 -> CV_RETR_TREE

		Trackbar contour area: sets the minimum area size of a contour to be shown

	"""


	# img is obtained as follows: load image -> converted to gray -> threshold binary(threshold = 128, maxval = 255)
	img = cv2.threshold(cv2.cvtColor(cv2.imread('../../img/stop.jpg'),cv2.cv.CV_RGB2GRAY), 128, 255, cv2.THRESH_BINARY)[1]

	# a black canvas of the size of the image to draw the contours
	canvas = np.zeros((img.shape[0],img.shape[1],3),np.uint8)

	#create a window
	cv2.namedWindow("panel",cv2.cv.CV_WINDOW_NORMAL)

	cv2.cv.MoveWindow("panel",img.shape[1],int(img.shape[0]*1.5))

	cv2.createTrackbar("mode","panel",0,3,dummy)
	# dictionary with the four constants for mode
	modeDict = {0:cv2.cv.CV_RETR_EXTERNAL,
		1:cv2.cv.CV_RETR_LIST ,
		2:cv2.cv.CV_RETR_CCOMP ,
		3:cv2.cv.CV_RETR_TREE}
	#create a trackbar to select contours with bigger or equal area than this trackbar position
	#if the trackbar is at maximum, then all the contours are shown (should be like trackbar at 0)
	trackbarMax=7000
	cv2.createTrackbar("contour Area","panel",10,trackbarMax,dummy)
    
	#trackbars to select the color for the hulls
	cv2.createTrackbar("b","panel",10,255,dummy)
	cv2.createTrackbar("g","panel",10,255,dummy)
	cv2.createTrackbar("r","panel",10,255,dummy)

	while True:	

		defectCanvas = canvas.copy()

		#calculate the contours	
		rawContours,hierarchy = cv2.findContours(img.copy(),modeDict[cv2.getTrackbarPos("mode","panel")],cv2.CHAIN_APPROX_SIMPLE)

		defects = []
		for cnt in rawContours:
			if cv2.contourArea(cnt,False)>=cv2.getTrackbarPos("contour Area","panel"):
				defect = cv2.cv.ConvexityDefects(cv2.cv.fromarray(cnt),cv2.convexHull(cnt),cv2.cv.fromarray(cnt))
				defects.append(defect)

		#polyAndHull = [(cv2.approxPolyDP(cnt,3,True),cv2.convexHull(cnt)) if cv2.contourArea(cnt,False)>=cv2.getTrackbarPos("contour Area","panel") else None for cnt in rawContours]
		
		#if not polyAndHull:
		#	print "polyAndHull vacio"

		#for pair in polyAndHull:
		#	print cv2.cv.ConvexityDefects(pair[0],pair[1],defect)

		#if not defects:
		#	print "vacio"

		#fill the hulls with the selected color
		#hulls = [pair[1] for pair in polyAndHull]

		#cv2.drawContours(defectCanvas,hulls,-1,
		#	(cv2.getTrackbarPos("b","panel"),cv2.getTrackbarPos("g","panel"),cv2.getTrackbarPos("r","panel")),
		#	cv2.cv.CV_FILLED)
		#paint the polinoms over the hulls
		cv2.drawContours(defectCanvas,defects,-1,(255,255,255))

		

		#cv2.imshow("passed img transformed",img)
		cv2.imshow("defects",defectCanvas)

		
		if (cv2.waitKey(5)!=-1):
			break






















