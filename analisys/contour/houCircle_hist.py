import cv2
import numpy as np


def change8bitMethod(x):
	global method
	if x==0:
		method = "adaptative threshold"
	elif x==1:
		method = "gaussianBlur"
	elif x == 2:
		method = "threshold"

def labelImg(img):
	global method
	black = (0,0,0)
	white = (255,255,255)
	point = (10,40)
	cv2.putText(img, method, point, cv2.FONT_HERSHEY_SIMPLEX,
	 1, white, 4)
	cv2.putText(img, method, point, cv2.FONT_HERSHEY_SIMPLEX,
	 1, black, 1)
	return img

def dummy(x):
	print x

if __name__ == "__main__":

	camera = cv2.VideoCapture(0)
	
	cv2.namedWindow("panel",cv2.cv.CV_WINDOW_NORMAL)

	method = "gaussianBlur"
	cv2.createTrackbar("to8bitMethod","panel",1,2,change8bitMethod)
	

	adaptMethDict = {0:cv2.ADAPTIVE_THRESH_MEAN_C,1:cv2.ADAPTIVE_THRESH_GAUSSIAN_C}
	cv2.createTrackbar("threshold adaptMeth","panel",0,1,dummy)
	cv2.createTrackbar("threshold maxval","panel",0,255,dummy)
	cv2.createTrackbar("threshold blocksize","panel",0,20,dummy)
	cv2.createTrackbar("threshold C","panel",0,20,dummy)

	cv2.createTrackbar("threshold thresh","panel",0,255,dummy)

	cv2.createTrackbar("gaussianBlur ksizeX","panel",0,20,dummy)
	cv2.createTrackbar("gaussianBlur ksizeY","panel",0,20,dummy)
	cv2.createTrackbar("gaussianBlur sigma1","panel",0,20,dummy)

	cv2.createTrackbar("dp","panel",1,2,dummy)
	cv2.createTrackbar("minDist","panel",200,500,dummy)

	while True:

		img = camera.read()[1]
		imgCopy = img.copy()
		imgCopy = cv2.cvtColor(imgCopy,cv2.cv.CV_RGB2GRAY)
		imgHist = imgCopy.copy()

		#calculates the 8 bit single channel image needed for the houCircle method
		if method == "adaptative threshold":

			adaptMeth = adaptMethDict[cv2.getTrackbarPos("threshold adaptMeth","panel")]
			maxval = cv2.getTrackbarPos("threshold maxval","panel")
			blocksize = 3+2*cv2.getTrackbarPos("threshold blocksize","panel")
			valueC = cv2.getTrackbarPos("threshold C","panel")

			imgCopy = cv2.adaptiveThreshold(imgCopy,
			 maxval, adaptMeth,cv2.THRESH_BINARY,blocksize,valueC)

		elif method == "gaussianBlur":
			ksize = (3+2*cv2.getTrackbarPos("gaussianBlur ksizeX","panel"),
				3+2*cv2.getTrackbarPos("gaussianBlur ksizeY","panel"))
			sigma1 = cv2.getTrackbarPos("gaussianBlur sigma1","panel")
	
			imgCopy = cv2.GaussianBlur(imgCopy, ksize, sigma1) 

		else:
			maxval = cv2.getTrackbarPos("threshold maxval","panel")
			thresh = cv2.getTrackbarPos("threshold thresh","panel")
			
			imgCopy = cv2.threshold(imgCopy, thresh, maxval, cv2.THRESH_BINARY)[1]


		cv2.imshow("8 bit img",labelImg(cv2.flip(imgCopy,1)))

		#calculates the histogram
		h = np.zeros((300,256,3));
		bins = np.arange(257)
		bin = bins[0:-1]
		color = [ (255,0,0),(255,255,255) ]
	
		for item,col in zip([imgHist,imgCopy],color):
			N,bins = np.histogram(item,bins)
			v=N.max()
			N = np.int32(np.around((N*255)/v))
			N=N.reshape(256,1)
			pts = np.column_stack((bin,N))
			cv2.polylines(h,np.array([pts],np.int32),False,col,2)

		h=np.flipud(h)
		cv2.imshow('histogram',h)




		#calculates the houCircles
		dp = cv2.getTrackbarPos("dp","panel")+1
		minDist = cv2.getTrackbarPos("minDist","panel")

		circles = []
		circles = cv2.HoughCircles(imgCopy, cv2.cv.CV_HOUGH_GRADIENT, dp, minDist)

		if not circles == None:
			circles = circles[0]
			for circle in circles:		
				center = (int(circle[0]),int(circle[1]))
				radius = circle[2]

				cv2.circle(img, center, radius, (255,255,255))



		cv2.imshow("detected circles",labelImg(cv2.flip(img,1)))

		if cv2.waitKey(5)!= -1:
			break
