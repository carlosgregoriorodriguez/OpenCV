import cv2
import numpy as np
from common import clock

def dummy(x):
	print x

MHI_DURATION = 0.5
MAX_TIME_DELTA = 0.25
MIN_TIME_DELTA = 0.05

if __name__ == '__main__':

	camera = cv2.VideoCapture(0)

	img = camera.read()[1]

	#create the motion history (mhi) of the same size as the image
	motionHist = np.zeros((img.shape[0], img.shape[1]), np.float32)

	firstTime = False

	while True:
		img = camera.read()[1]
		img = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)
		#create the silhouette with adaptative threshold
		silhouette = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
			cv2.THRESH_BINARY,7,10)
		
		timestamp = clock()
		cv2.updateMotionHistory(silhouette, motionHist, timestamp, MHI_DURATION)
		
		mask,orientation = cv2.calcMotionGradient(motionHist,MAX_TIME_DELTA,MIN_TIME_DELTA)
	
		if not firstTime:
			print mask.shape
			print orientation.shape
			firstTime = True
			print mask
			
		cv2.imshow("motionHist",motionHist)
		cv2.imshow("mask",mask)
		cv2.imshow("orientation",orientation)

		if (cv2.waitKey(5)!=-1):
			break