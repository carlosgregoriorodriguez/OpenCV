import cv2
import numpy as np


def dummy(x):
	print x

def showboth(hist,hist_item):
	print "showboth"
	for item,itemHI in zip(hist,hist_item):
		print [item[0],itemHI[0]]

def labelImg(img,label):
	black = (0,0,0)
	white = (255,255,255)
	point = (10,40)
	cv2.putText(img, label, point, cv2.FONT_HERSHEY_SIMPLEX,
	 1, white, 4)
	cv2.putText(img, label, point, cv2.FONT_HERSHEY_SIMPLEX,
	 1, black, 1)
	return img

if __name__ == "__main__":

	camera = cv2.VideoCapture(0)
	
	cv2.namedWindow("panel",cv2.cv.CV_WINDOW_NORMAL)

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

		h = np.zeros((300,255,3))
		bins = np.arange(256).reshape(256,1)

		hist_item = cv2.calcHist(imgCopy,[0],None,[256],[0,255])
		scalar = imgCopy.shape[0]*imgCopy.shape[1]
		hist = hist_item.copy()

		for i in range(256):
			hist_item[i] = hist_item[i]/scalar

		
		pts = np.column_stack((bins,hist))
		cv2.polylines(h,np.array([pts],np.int32),False,(0,0,255))

		h=np.flipud(h)

		cv2.imshow("histogram",h)

		sumAcumulator = 0
		threshIndex = 0

		#showboth(hist,hist_item)
		

		for i in range(255):
			sumAcumulator +=hist[i]
			if sumAcumulator>=0.5:
				threshIndex = i
				break

		cv2.imshow("original",imgCopy)
		cv2.imshow("thresholded",
			labelImg(cv2.threshold(imgCopy, 
				threshIndex, 255, cv2.THRESH_BINARY)[1],str(threshIndex)))





		# dp = cv2.getTrackbarPos("dp","panel")+1
		# minDist = cv2.getTrackbarPos("minDist","panel")
		# param1 = cv2.getTrackbarPos("param1","panel")+1
		# param2 = cv2.getTrackbarPos("param2","panel")+1
		# minRadius = cv2.getTrackbarPos("minRadius","panel")
		# maxRadius = cv2.getTrackbarPos("maxRadius","panel")

		# circles = []
		# circles = cv2.HoughCircles(imgCopy, cv2.cv.CV_HOUGH_GRADIENT,
		#  dp, minDist, param1 = param1, param2 = param2,
		#   minRadius = minRadius, maxRadius = maxRadius)

		# if not circles == None:
		# 	circles = circles[0]
		# 	for circle in circles:
		# 		center = (circle[0],circle[1])
		# 		radius = circle[2]	
		# 		cv2.circle(img, center, 3, (0,0,255))
		# 		cv2.circle(img, center, radius, (255,255,255))


		# cv2.imshow("detected circles",cv2.flip(img,1))

		if cv2.waitKey(5)!= -1:
			break
