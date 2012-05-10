import cv2
import numpy as np
import sys
from glob import glob



def dummy(x):
	print x



def render(img):
	copy = img.copy()
	squares = []
	for i in range(img.shape[1]/50):
		aux = []
		for j in range(img.shape[0]/50):
			pt1=(i*50,j*50)
			pt2=((i+1)*50,(j+1)*50)
			cv2.rectangle(copy, pt1, pt2, (0,255,0), thickness=3)
			center = (i*50+25,j*50+25)
			aux.append(cv2.getRectSubPix(img, (25,25), center))
		squares.append(aux)
	return copy,squares


def getHistogram(img):
	img = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)
	hist_item = cv2.calcHist([img],[0],None,[256],[0,255]) 	
	cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)	
	return hist_item



def getDistances(selectedElement,allElements):
	distanceMatrix = []
	for column in allElements:
		c = []
		for element in column:
			distance = cv2.compareHist(getHistogram(selectedElement),getHistogram(element),cv2.cv.CV_COMP_BHATTACHARYYA)
			c.append(distance)
		distanceMatrix.append(c)
	return distanceMatrix



def showDistances(distanceMatrix):
	width = len(distanceMatrix)
	if width>0:
		height = len(distanceMatrix[0])
		canvas = np.zeros((height*50,width*50,3),np.uint8)
		for column in enumerate(distanceMatrix):
			for element in enumerate(column[1]):
				#the element is between 0 and 1. 0 best, 1 worst
				canvas[element[0]*50:(element[0]+1)*50,column[0]*50:(column[0]+1)*50,:]= np.ones((50,50,3))*int(255*element[1])
				cv2.putText(canvas, str(round(element[1],3)) , (column[0]*50+20,element[0]*50+30),
				 cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)
		return canvas,True
	return np.zeros((10,10)),False


def resize(img):
	w =min(450,img.shape[1])
	imgH,imgW = img.shape[:2]
	divConstant = imgW/w
	return cv2.resize(img,(w,int(imgH/divConstant)))

def relocate(x,y,img):
	w =min(450,img.shape[1])
	imgH,imgW = img.shape[:2]
	divConstant = imgW/w
	x*=divConstant
	y*=divConstant



if __name__ == "__main__":
	path = '../images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])
	showImg,squares = render(img)
	
	distanceMatrix=[]

	# method for the mouse event
	def onmouse(event, x, y, flags, param):
		global distanceMatrix
		global img
		relocate(x,y,img)
		if flags & cv2.EVENT_FLAG_LBUTTON:
			column = x/50
			row = y/50
			selectedSquare = squares[column][row]
			distanceMatrix = getDistances(selectedSquare,squares)

	cv2.namedWindow('image',cv2.cv.CV_WINDOW_AUTOSIZE)
	cv2.setMouseCallback('image', onmouse)
	
	while True:	

		cv2.imshow('image',resize(showImg))
		auxImg = resize(showDistances(distanceMatrix)[0])
		cv2.imshow('distances',auxImg)
		
		key = cv2.waitKey(5)
	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
	 		showImg,squares=render(img)
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])
	 		showImg,squares=render(img)
	 	elif (key != -1):
	 		break


