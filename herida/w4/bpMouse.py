import cv2
import numpy as np
import sys
from glob import glob


def getHist(img):
	img = cv2.cvtColor(img,cv2.cv.CV_BGR2HSV)
	#hueImg,satImg = cv2.split(img)[:2]
	imgArray = [img,]
	channels = [0,1]
	histSize = [30,32]
	ranges = [0,180,0,256]
	hist = cv2.calcHist(imgArray,channels,None,histSize,ranges) 
		
	#normalize the histogram
	x = 0
	for hueIndex in range(histSize[0]):
		for satIndex in range(histSize[1]):
			x+=hist[hueIndex][satIndex]
	y=0
	for hueIndex in range(histSize[0]):
		for satIndex in range(histSize[1]):
			hist[hueIndex][satIndex]=round((hist[hueIndex][satIndex]/x)*100,2)
			y+=hist[hueIndex][satIndex]

	scale = 20
	normCanvas = np.zeros((histSize[0]*scale,histSize[1]*scale,3),np.uint8)
	for hueIndex in range(histSize[0]):
		for satIndex in range(histSize[1]):
			patch = np.ones((scale,scale,3),np.uint8)*hist[hueIndex][satIndex]*255
			normCanvas[hueIndex*scale:(hueIndex+1)*scale,satIndex*scale:(satIndex+1)*scale,:]=patch
			
	return hist,normCanvas


if __name__ == "__main__":
	
	path = '../images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])
	img = cv2.resize(img,(min(img.shape[1],1250),min(img.shape[0],750)))
	
	showImg = img.copy()
	bp = np.zeros((img.shape),np.uint8)

	cv2.namedWindow('image',cv2.cv.CV_WINDOW_AUTOSIZE)
	
	def onmouse(event, x, y, flags, param):
		global img
		global showImg
		global bp
		showImg = img.copy()
		center = (x,y)
		pt1 = (x-25,y-25)
		pt2 = (x+25,y+25)
		cv2.rectangle(showImg, pt1, pt2, (0,0,255), thickness=2)
		patch = cv2.getRectSubPix(img, (25,25), center)
		if flags & cv2.EVENT_FLAG_LBUTTON:
			getHist(patch)[0]
			aux = cv2.calcBackProject([cv2.cvtColor(img,cv2.cv.CV_BGR2HSV)],
				[0,1], getHist(patch)[0], [0,180,0,256],1)
			thresh_ret,bp = cv2.threshold(aux,1,255,cv2.THRESH_BINARY)

	cv2.setMouseCallback('image', onmouse)

	while True:	

		cv2.imshow('image',showImg)
		cv2.imshow('bp',bp)

		key = cv2.waitKey(5)
	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
	 		img = cv2.resize(img,(min(img.shape[1],1250),min(img.shape[0],750)))
	 		showImg = img.copy()
	 		bp = np.zeros((img.shape),np.uint8)
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])
	 		img = cv2.resize(img,(min(img.shape[1],1250),min(img.shape[0],750)))
	 		showImg = img.copy()
	 		bp = np.zeros((img.shape),np.uint8)
	 	elif (key != -1):
	 		break

























