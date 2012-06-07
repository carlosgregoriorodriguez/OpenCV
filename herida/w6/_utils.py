import cv2
import numpy as np


#applies a threshold such that if x is in interval=[a,b] then x remains, else x :=0.
#a and b are included and [a,b] is in [0,infinit]
#for setting interval=[a,infinit] set b=-1
def intervalThreshold(img,interval):
	img = cv2.threshold(img,interval[0]-1,255,cv2.cv.CV_THRESH_TOZERO)[1]
	if interval != -1:
		img = cv2.threshold(img,interval[1],255,cv2.cv.CV_THRESH_TOZERO_INV)[1]
	return img

if __name__ == "__main__":
	print 'only methods'