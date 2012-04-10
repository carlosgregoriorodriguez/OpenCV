

#This example is not working as it should when goodFeaturesToTrack is called.
#The error is commented


import cv2
import numpy as np


def dummy(x):
	print x

if __name__ == "__main__":

	camera = cv2.VideoCapture(0)

	#get the previous image from which the good features are taken
	prevImg = camera.read()[1]
	prevImg = cv2.cvtColor(prevImg,cv2.cv.CV_RGB2GRAY)

	cv2.namedWindow("panel",cv2.cv.CV_WINDOW_NORMAL)
	cv2.cv.MoveWindow("panel",prevImg.shape[1],int(prevImg.shape[0]*1.5))
	cv2.createTrackbar("maxCorners","panel",5,100,dummy)
	cv2.createTrackbar("qualityLevel","panel",10,100,dummy)
	cv2.createTrackbar("minDistance","panel",5,100,dummy)

	#get the previous good features
	prevVect = cv2.goodFeaturesToTrack(prevImg,
		cv2.getTrackbarPos("maxCorners","panel"),
		#float((cv2.getTrackbarPos("qualityLevel","panel")+1)/100),
		0.001,
		cv2.getTrackbarPos("minDistance","panel"))

	while True:
		original = camera.read()[1]
		#get the next image or calcOpticalFlowPyrLK
		nextImg = cv2.cvtColor(original,cv2.cv.CV_RGB2GRAY)
		#compute calcOpticalFlowPyrLK
		nextVect = np.copy(prevVect)
		nextVect , status , err = cv2.calcOpticalFlowPyrLK(prevImg,nextImg,prevVect,nextVect)

		#for every good feature we paint it
		for i in range(prevVect.shape[0]):
			if status[i][0]==1:
				p1 = (int(prevVect[i][0][0]),int(prevVect[i][0][1]))
				p2 = (int(nextVect[i][0][0]),int(nextVect[i][0][1]))
				
				if p1!=p2:
					cv2.circle(original, p1 ,3 , (255,0,0))
					cv2.circle(original, p2 ,3 , (0,0,255))
					cv2.line(original,p1,p2,(0,0,0),3)
				else:
					cv2.circle(original, p1 ,3 , (0,0,255))
			else:
				p1 = (int(prevVect[i][0][0]),int(prevVect[i][0][1]))
				cv2.circle(original, p1 ,3 , (255,255,255))


		prevImg = nextImg.copy()
		prevVect = cv2.goodFeaturesToTrack(prevImg,
			cv2.getTrackbarPos("maxCorners","panel"),
			#float((cv2.getTrackbarPos("qualityLevel","panel")+1)/100),
			0.001,
			cv2.getTrackbarPos("minDistance","panel"))

		cv2.imshow("original",original)

		if (cv2.waitKey(5)!=-1):
			break
