#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
          
def dummy(v):
	print "value "+str(v)

def labeledImg(img,name):
	cv2.putText(img,name,(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,1,1,8,False)
	return img



if __name__ == "__main__":

	camera = cv2.VideoCapture(0)

	#create the window where the thresholded image will be shown
	cv2.namedWindow("split")

    #create a trackbar that controlls the thresh value
	cv2.createTrackbar("channel","split",0,2,dummy)

	d = {0:"Red Channel",1:"Green Channel",2:"Blue Channel"}

	while True:

		f,img = camera.read()
		cv2.imshow("original",img)

		cv2.imshow("split",labeledImg(cv2.split(img)[cv2.getTrackbarPos("channel","split")],d[cv2.getTrackbarPos("channel","split")]))

		if (cv2.waitKey(5) != -1):
			break
