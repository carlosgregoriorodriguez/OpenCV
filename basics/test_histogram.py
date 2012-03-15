#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import numpy as np


def getPolishedHist(img):
	img = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)

	hist_item = cv2.calcHist([img],[0],None,[256],[0,255]) 
		
	cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
		
	return hist_item
	#return np.int32(np.around(hist_item))

          
if __name__ == "__main__":

	camera = cv2.VideoCapture(0)
	
	#creamos una matriz de tres canales de ceros (una imagen negra) sobre la que vamos a pintar
	#h = np.zeros((300,256,3))
	#dividimos la imagen en sus tres canales

	bins = np.arange(256).reshape(256,1)

	f,img = camera.read()
		
	actualHist=getPolishedHist(img)

	cv2.imshow("first im",img)

	lastHist = actualHist

	# print type(actualHist)
	# print type(lastHist)

	# print actualHist.shape
	# print lastHist.shape

	# print actualHist[0][0]

	# print type(actualHist[0][0])
	# print type(lastHist[0][0])



	while True:

		f,img = camera.read()
		
		actualHist=getPolishedHist(img)
		
		cv2.imshow("webcam",img)

		key = cv2.waitKey(10)

		if (key==104):

			distHist = cv2.compareHist(actualHist,lastHist,cv2.cv.CV_COMP_CHISQR)

			print distHist

		

			#lastHist = actualHist

			cv2.imshow("webcamFrame",img)


		#pts = np.column_stack((bins,hist))
		
		#cv2.polylines(h,np.array([pts],np.int32),False,(255,0,0))
		
		#cv2.imshow("webcam",img)
		
		#h=np.flipud(h)

		#cv2.imshow('colorhist',h)
		
		if (key == 27):
			break

