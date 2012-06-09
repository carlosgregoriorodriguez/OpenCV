import cv2
import numpy as np
from time import clock
from _utils import *


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


def getSignificantRegions(img,sqHist):
	totalH,totalW = img.shape[0],img.shape[1]
	rowNum,colNum = sqHist.shape[:2]
	lh,lw = totalH/rowNum,totalW/colNum
	
	returnList = []
	for row in range(rowNum):
		for col in range(colNum):
			if sqHist[row][col]!=0:
				returnList.append(img[row*lh:(row+1)*lh,col*lw:(col+1)*lw])
	return returnList




#this method gets the areas in the image corresponding to significant squares and computes the
#hs-histogram for every area.
#With the histogram it calculates the backproyection for the complete image.
#Every backproyection is then thresholded with a binary threshold where the parameter thresh is 
#probThresh. Every pixel with a probability higher than probThresh of having a similar 
#histogram gets a value of 255.
#A mask is build considering the maximal value of all the bp.
#Only the connected component nearest to the center is considered in the mask.
def bpSignificantSquares(img,sigSquares,probThresh):
	print '-BP-'
	#get a list of the regions of the image for which the histogram for backproyection will be calculated
	print '-BP-getRegionList'
	myTime = clock()
	regionList = getSignificantRegions(img,sigSquares)
	print '-BP- len of regionList: '+str(len(regionList))
	print '-BP- ===>takes '+str(clock()-myTime)
	myTime = clock()

	mask = np.zeros((img.shape[:2]),np.uint8)

	print '-BP-gethist and bp'
	myTime = clock()
	for region in regionList:
		hist = getHist(region)[0]
		aux = cv2.calcBackProject([cv2.cvtColor(img,cv2.cv.CV_BGR2HSV)],
			[0,1], hist, [0,180,0,256],1)
		bp = cv2.threshold(aux,probThresh,255,cv2.THRESH_BINARY)[1]
		mask = cv2.max(mask,bp)
	print '-BP- ===>takes '+str(clock()-myTime)
	myTime = clock()

	aux = np.zeros((mask.shape),np.uint8)
	print '-BP-getComponentOf '
	aux = getComponentOf(mask,(mask.shape[1]/2,mask.shape[0]/2),True)
	print '-BP- ===>takes '+str(clock()-myTime)
	myTime = clock()

	return cv2.merge([mask,]*3) , cv2.merge([aux*255,]*3)


# def getCenterComponent(mask):
# 	rows,cols = mask.shape[:2]
# 	aux = cv2.minMaxLoc(mask[rows/2-10:rows/2+10,cols/2-10:cols/2+10])
# 	centerValue,center = aux[1],aux[3]
# 	x = center[0]+cols/2-10
# 	y = center[1]+rows/2-10
# 	center = (x,y)
# 	print 'centerValue '+str(centerValue)+' at '+str(center)
# 	outVal = 50
# 	auxMask = np.zeros((rows+2,cols+2),np.uint8)	
# 	cv2.floodFill(mask, auxMask, center, [outVal,]*3,[5,]*3,[5,]*3,cv2.cv.CV_FLOODFILL_FIXED_RANGE)
# 	mask = cv2.threshold(mask,outVal-1,255,cv2.cv.CV_THRESH_TOZERO)[1]
# 	mask = cv2.threshold(mask,outVal+1,255,cv2.cv.CV_THRESH_TOZERO_INV)[1]
# 	mask = cv2.threshold(mask,1,255,cv2.cv.CV_THRESH_BINARY)[1]
# 	mask = cv2.adaptativeThreshold()
# 	return mask


if __name__ == "__main__":
	print 'only methods'









	
