import cv2
import numpy as np
import sys
from glob import glob



def dummy(x):
	print x


#takes an image, first it makes a copy resized to fit the screen to show.
#then it paints a grid (50x50) on the resized copy and creates a 50x50 matrix
#with the subrectangles of the image, corresponding to the tiles of the grid.
def render(img,sqNum):
	print 'in render'
	copy = img.copy()
	
	#resize the copy
	#while (copy.shape[0]>900 or copy.shape[1]>900):
	#	copy = cv2.pyrDown(copy)

	#paint the grid
	copyY,copyX = copy.shape[:2]
	for i in range(1,sqNum-1):
		ptX=i*copyX/sqNum
		cv2.line(copy, (ptX,0), (ptX,copyY), (255,0,0), thickness=1)
		ptY=i*copyY/sqNum
		cv2.line(copy, (0,ptY), (copyX,ptY), (255,0,0), thickness=1)
	
	#get the histograms of the corresponding tiles
	l = copyX/(2*sqNum)
	h = copyY/(2*sqNum)
	squares = []
	for i in range(0,sqNum-1):
		aux = []
		for j in range(0,sqNum-1):
			center = (i*copyX/sqNum+l,j*copyY/sqNum+h)
			aux.append(getHist(cv2.getRectSubPix(img, (l,h), center))[0])
		squares.append(aux)
	return copy,squares


#computes a normalized histogram of an image.
def getHist(img):
	print 'in getHist'
	img = cv2.cvtColor(img,cv2.cv.CV_RGB2HSV)
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


#computes the BHATTACHARYYA distance for all tiles of squares compared to the selected square
def getDistances(selectedElement,allElements):
	print 'in getDistances'
	distanceMatrix = []
	for column in allElements:
		c = []
		for element in column:
			distance = cv2.compareHist(selectedElement,element,cv2.cv.CV_COMP_BHATTACHARYYA)
			c.append(distance)
		distanceMatrix.append(c)
	return distanceMatrix



def showDistances(distanceMatrix,shape,sqNum):
	print 'in showDistances'
	w=shape[1]/sqNum
	h=shape[0]/sqNum
	if len(distanceMatrix)>0:
		canvas = np.zeros((shape[0],shape[1],3),np.uint8)
		for column in enumerate(distanceMatrix):
			for element in enumerate(column[1]):
				#the element is between 0 and 1. 0 best, 1 worst
				canvas[element[0]*h:(element[0]+1)*h,column[0]*w:(column[0]+1)*w,:]= np.ones((h,w,3))*int(255*element[1])
				#cv2.putText(canvas, str(round(element[1],3)) , (column[0]*w+20,element[0]*h+30),
				# cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)
		return canvas,True
	return np.zeros((10,10)),False



if __name__ == "__main__":
	path = '../images/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.cvtColor(cv2.imread(imageNames[imgIndex]),cv2.cv.CV_BGR2HSV)
	img = cv2.resize(img,(min(img.shape[1],1250),min(img.shape[0],750)))
	sqNum = 20
	showImg,squares = render(img,sqNum)
	
	distanceMatrix=[]

	# method for the mouse event
	def onmouse(event, x, y, flags, param):
		global distanceMatrix
		global showImg
		global squares
		global sqNum

		w=showImg.shape[1]/sqNum
		h=showImg.shape[0]/sqNum

		if flags & cv2.EVENT_FLAG_LBUTTON:
			column = x/w
			row = y/h
			selectedSquare = squares[column][row]
			distanceMatrix = getDistances(selectedSquare,squares)

	cv2.namedWindow('image',cv2.cv.CV_WINDOW_AUTOSIZE)
	cv2.setMouseCallback('image', onmouse)
	
	while True:	

		cv2.imshow('image',showImg)
		auxImg = showDistances(distanceMatrix,showImg.shape[:2],sqNum)[0]
		cv2.imshow('distances',auxImg)
		
		key = cv2.waitKey(5)
	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
 			img = cv2.resize(img,(min(img.shape[1],1250),min(img.shape[0],750)))
	 		showImg,squares=render(img,sqNum)
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])
 			img = cv2.resize(img,(min(img.shape[1],1250),min(img.shape[0],750)))
	 		showImg,squares=render(img,sqNum)
	 	elif (key != -1):
	 		break


