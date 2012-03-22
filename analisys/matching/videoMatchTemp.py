import cv2
import numpy as np
import sys



def dummy(x):
	print x

def getSquareLimits(img):
	rows = img.shape[0]
	cols = img.shape[1]

	rowsUp = rows/3
	rowsDown = 2*rowsUp

	colsLeft = cols/3
	colsRight = 2*colsLeft

	return (rowsUp,rowsDown,colsLeft,colsRight)

def paintLimits(img,squareLimits):
	imgCopy=img.copy()
	cv2.rectangle(imgCopy,(squareLimits[1],squareLimits[3]),(squareLimits[0],squareLimits[2]),(0,255,0))
	return imgCopy


if __name__ == "__main__":

	camera = cv2.VideoCapture(0)
	
	squareLims = getSquareLimits(camera.read()[1])

	#create a window
	cv2.namedWindow("matchTemplate")    
	#create a trackbar that controlls the method argument of the function matchTemplate
	cv2.createTrackbar("method","matchTemplate",0,4,dummy)
	# dictionary with the constants for method
	methodDict = {0:cv2.cv.CV_TM_SQDIFF_NORMED,
		1:cv2.cv.CV_TM_CCORR ,
		2:cv2.cv.CV_TM_CCORR_NORMED ,
		3:cv2.cv.CV_TM_CCOEFF,
		4:cv2.cv.CV_TM_CCOEFF_NORMED}
	
	fixedTemp = False


	while True:		
		
		img = camera.read()[1]
		
		key = cv2.waitKey(5)

		if (key == 32):
			#takes the template from the image
			fixedTemp = True
			template = cv2.getRectSubPix(img,
				(squareLims[1]-squareLims[0],squareLims[3]-squareLims[2]),
				(img.shape[0]/2,img.shape[1]/2))


		if fixedTemp:
			#looks for the best match
			foundTemp = cv2.matchTemplate(img,template,
				methodDict[cv2.getTrackbarPos("method","matchTemplate")])

			cv2.imshow("template",template)
			cv2.imshow("foundTemp",foundTemp)
			minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(foundTemp)
			
			#marks the best match
			cv2.rectangle(img,minLoc,(minLoc[0]+template.shape[1],minLoc[1]+template.shape[0]),(0,255,0))


		cv2.imshow("matchTemplate",paintLimits(img,squareLims))



		if (key==113):
			break













