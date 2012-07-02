import cv2
import numpy as np
import sys
from glob import glob
from time import clock
import pickle

from findStaples import findStaplesMethod

def eventCols(x):
	global cols,selectedImg
	cols = x
	selectedImg=-1
	setDimensions()
	print x


def eventW(x):
	global w,selectedImg
	w = x
	selectedImg=-1
	setDimensions()
	print x


def eventH(x):
	global h,selectedImg
	h = x
	selectedImg=-1
	setDimensions()
	print x


def setDimensions():
	global spaceW,imgW,spaceH,imgH,icons
	spaceW = int(w/cols)
	imgW = int(spaceW/3)
	spaceH = int(h/((len(imageNames)/cols)+1))
	imgH = int(spaceH/3)
	icons = setIcons()


def setIcons():
	icons = []
	for name in imageNames:
		icons.append(cv2.resize(cv2.imread(name),(imgW,imgH)))
	return icons


def getSelectedImg(mousePos):
	return int(mousePos[0]/spaceW)+int(mousePos[1]/spaceH)*cols


def buildDisplay(selectedImg):
	background = np.zeros((h,w,3),np.uint8)
	print 'antes del for '+str(clock())
	for i in range(len(imageNames)):
		globPos = (i%cols,int(i/cols))
		imgPos = (globPos[0]*spaceW,globPos[1]*spaceH)
		if i!=selectedImg:
			img = icons[i]
			background[imgPos[1]+imgH:imgPos[1]+2*imgH,imgPos[0]+imgW:imgPos[0]+2*imgW,:]=img
		else:
			img = cv2.resize(cv2.imread(imageNames[i]),(spaceW,spaceH))
			background[imgPos[1]:imgPos[1]+spaceH,imgPos[0]:imgPos[0]+spaceW,:]=img
	print 'despues del for '+str(clock())
	return background




if __name__ == "__main__":

	path = '../images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])	
	
	f = open('parameters','r')
	parameterDict = pickle.load(f)
	f.close()

	
	cv2.namedWindow('panel',cv2.cv.CV_WINDOW_NORMAL)
	cv2.namedWindow('display',cv2.cv.CV_WINDOW_AUTOSIZE)
	cv2.namedWindow('method window',cv2.cv.CV_WINDOW_NORMAL)
	cv2.createTrackbar('width','panel',900,2000,eventW)
	cv2.createTrackbar('height','panel',750,2000,eventH)
	cv2.createTrackbar('cols','panel',5,10,eventCols)

	h=cv2.getTrackbarPos('height','panel')
	w=cv2.getTrackbarPos('width','panel')
	cols=cv2.getTrackbarPos('cols','panel')
	icons = []
	setDimensions()
	
	selectedImg = -1
	method = 'notSelected'

	def onmouse(event, x, y, flags, param):
		global display,selectedImg

		aux = getSelectedImg((x,y))
		if selectedImg != getSelectedImg((x,y)):
			selectedImg = aux
			display = buildDisplay(selectedImg)

		if flags & (event == cv2.EVENT_FLAG_LBUTTON):
			print 'click at '+str((x,y))
			if method!='notSelected':
				#cv2.destroyWindow('display')
				imgIndex,imageNames,parameterDict
				findStaplesMethod(selectedImg,imageNames,parameterDict)
				display = buildDisplay(selectedImg)

	cv2.setMouseCallback('display', onmouse)

	display = buildDisplay(selectedImg)

	while True:
		
		cv2.imshow('display',display)
	 	
	 	key = cv2.waitKey(5)
	 	if (key==120):
	 		print '1'
	 	elif (key==122):
	 		print '2'
	 	elif (key == 114): # key == 'r'
	 		icons = setIcons()
	 	elif (key == 49):
	 		method = 'findStaples'
	 		print 'select an image to apply findStaples'
	 	elif (key != -1):
	 		break









	
