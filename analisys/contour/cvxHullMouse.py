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
	# and a copy is made for the later painting
	canvas = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
	canvasAux = canvas.copy()

	#create a window
	cv2.namedWindow("panel",cv2.cv.CV_WINDOW_NORMAL)
	cv2.cv.MoveWindow("panel",img.shape[1],int(img.shape[0]*1.5))

	cv2.createTrackbar("mode","panel",1,3,dummy)
	# dictionary with the four constants for mode
	modeDict = {0:cv2.cv.CV_RETR_EXTERNAL,
		1:cv2.cv.CV_RETR_LIST ,
		2:cv2.cv.CV_RETR_CCOMP ,
		3:cv2.cv.CV_RETR_TREE}
	#create a trackbar to select contours with bigger or equal area than this trackbar position
	#if the trackbar is at maximum, then all the contours are shown (should be like trackbar at 0)
	trackbarMax=7000
	cv2.createTrackbar("contour Area","panel",10,trackbarMax,dummy)
	cv2.createTrackbar("line","panel",3,5,dummy)    

	# create a window to add the mouse event
	cv2.namedWindow("hulls")


	# auxiliar method
	def toList(hull):
		pointList = [x[0] for x in hull]
		return pointList
		

	# method to calculate if a point is in a hull
	def inHull(point):
		for hull in sorted(bigHulls,key=cv2.contourArea):
			pointList = toList(hull)
			firstQ,secondQ,thirdQ,fourthQ = False,False,False,False
			for p in pointList:
				if (p[0]>=point[0] and p[1]>=point[1]):
					firstQ=1
				elif (p[0]<point[0] and p[1]>=point[1]):
					secondQ=1
				elif (p[0]<point[0] and p[1]<point[1]):
					thirdQ=1
				else:
					fourthQ=1

			if firstQ and secondQ and thirdQ and fourthQ:
				return hull


	hullOfPoint = None
	
	# method for the mouse event
	def onmouse(event, x, y, flags, param):
		global hullOfPoint
		if flags & cv2.EVENT_FLAG_LBUTTON:
			hullOfPoint = inHull((x,y))
			


	cv2.setMouseCallback("hulls", onmouse)


	
	while True:	
		canvasAux = canvas.copy()
		
		# calculate the contours	
		rawContours,hierarchy = cv2.findContours(img.copy(),modeDict[cv2.getTrackbarPos("mode","panel")],cv2.CHAIN_APPROX_SIMPLE)

		bigHulls = []
		for cnt in rawContours:
			area = cv2.contourArea(cnt,False)	
			if (area>=cv2.getTrackbarPos("contour Area","panel")):
				bigHulls.append(cv2.convexHull(cnt))
			
		# paint the contours of the hulls
		cv2.drawContours(canvasAux,bigHulls,-1,(255,255,255),cv2.getTrackbarPos("line","panel"))
		
		# if a hull was selected, fill it white
		if hullOfPoint!=None:
			#I don't know why, but I have to give two different elements to aux to make it work
			aux = (hullOfPoint,bigHulls[0])
			cv2.drawContours(canvasAux,aux,0,(255,255,255),cv2.cv.CV_FILLED)
			
		cv2.imshow("hulls",canvasAux)
		
		if (cv2.waitKey(5)!=-1):
			break


