import cv2
import numpy as np
import sys
from glob import glob
import math



def doAndPack(img):
	
	h, w = 475,550
	bfImg = cv2.bilateralFilter(img, 9, 400, 400)
	#cv2.cvtColor(bfImg,cv2.cv.CV_RGB2GRAY)

	background = np.zeros((h,w*3,3),np.uint8)
	background[0:h,0:w,0:3]=cv2.resize(img,(w,h))
	background[0:h,w:2*w,0:3]=cv2.resize(bfImg,(w,h))

	return background


if __name__ == "__main__":


	path = '../images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0

	slideShow = []
	for name in imageNames:
		slideShow.append(doAndPack(cv2.imread(name)))

	while True:

		cv2.imshow('original',slideShow[imgIndex])
		
		key = cv2.waitKey(5)

	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]

	 	elif (key != -1):
	 		break









	
