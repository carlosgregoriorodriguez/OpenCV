import cv2
import numpy as np


def dummy(x):
	print x

if __name__ == "__main__":

	camera = cv2.VideoCapture(0)
	
	cv2.namedWindow("panel",cv2.cv.CV_WINDOW_NORMAL)


	cv2.createTrackbar("threshold maxval","panel",255,255,dummy)
	cv2.createTrackbar("threshold thresh","panel",0,255,dummy)


	cv2.createTrackbar("dp","panel",1,2,dummy)
	cv2.createTrackbar("minDist","panel",200,500,dummy)
	cv2.createTrackbar("param1","panel",10,20,dummy)
	cv2.createTrackbar("param2","panel",200,500,dummy)
	cv2.createTrackbar("minRadius","panel",1,500,dummy)
	cv2.createTrackbar("maxRadius","panel",200,500,dummy)
	while True:

		img = camera.read()[1]
		imgCopy = img.copy()
		imgCopy = cv2.cvtColor(imgCopy,cv2.cv.CV_RGB2GRAY)

		maxval = cv2.getTrackbarPos("threshold maxval","panel")
		thresh = cv2.getTrackbarPos("threshold thresh","panel")

		imgCopy = cv2.threshold(imgCopy, thresh, maxval, cv2.THRESH_BINARY)[1]


		dp = cv2.getTrackbarPos("dp","panel")+1
		minDist = cv2.getTrackbarPos("minDist","panel")
		param1 = cv2.getTrackbarPos("param1","panel")
		param2 = cv2.getTrackbarPos("param2","panel")
		minRadius = cv2.getTrackbarPos("minRadius","panel")
		maxRadius = cv2.getTrackbarPos("maxRadius","panel")

		circles = []
		circles = cv2.HoughCircles(imgCopy, cv2.cv.CV_HOUGH_GRADIENT,
		 dp, minDist, param1 = param1, param2 = param2,
		  minRadius = minRadius, maxRadius = maxRadius)

		if not circles == None:
			circles = circles[0]
			for circle in circles:
				center = (circle[0],circle[1])
				radius = circle[2]	
				cv2.circle(img, center, radius, (255,255,255))


		cv2.imshow("detected circles",cv2.flip(img,1))

		if cv2.waitKey(5)!= -1:
			break
