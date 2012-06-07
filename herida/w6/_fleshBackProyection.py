import cv2
import numpy as np


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


def getCenterComponent(mask):
	rows,cols = mask.shape[:2]
	aux = cv2.minMaxLoc(mask[rows/2-10:rows/2+10,cols/2-10:cols/2+10])
	centerValue,center = aux[1],aux[3]
	x = center[0]+cols/2-10
	y = center[1]+rows/2-10
	center = (x,y)
	print 'centerValue '+str(centerValue)+' at '+str(center)
	outVal = 50
	auxMask = np.zeros((rows+2,cols+2),np.uint8)
	#auxMask[1:rows+1,1:cols+1]=auxMask[1:rows+1,1:cols+1]-mask
	
	cv2.floodFill(mask, auxMask, center, [outVal,]*3,[5,]*3,[5,]*3,cv2.cv.CV_FLOODFILL_FIXED_RANGE)
	mask = cv2.threshold(mask,outVal-1,255,cv2.cv.CV_THRESH_TOZERO)[1]
	mask = cv2.threshold(mask,outVal+1,255,cv2.cv.CV_THRESH_TOZERO_INV)[1]
	mask = cv2.threshold(mask,1,255,cv2.cv.CV_THRESH_BINARY)[1]
	#mask = auxMask[1:rows+1,1:cols+1]
	return mask


def bpSignificantSquares(img,sigSquares,probThresh):

	regionList = getSignificantRegions(img,sigSquares)

	mask = np.zeros((img.shape[:2]),np.uint8)

	for region in regionList:
		hist = getHist(region)[0]
		aux = cv2.calcBackProject([cv2.cvtColor(img,cv2.cv.CV_BGR2HSV)],
			[0,1], hist, [0,180,0,256],1)
		bp = cv2.threshold(aux,probThresh,255,cv2.THRESH_BINARY)[1]
		mask = cv2.max(mask,bp)
	

	aux = np.zeros((mask.shape),np.uint8)
	#aux = aux-mask
	#aux[:,:]=mask
	aux = getCenterComponent(mask)


	#return cv2.merge([cv2.min(mask,layer) for layer in cv2.split(img)])
	#
	#retList = []
	#retList.append(cv2.merge([mask,]*3))
	#retList.append(cv2.merge([aux,]*3))
	#return retList
	
	return cv2.merge([mask,]*3) , cv2.merge([aux,]*3)


if __name__ == "__main__":
	print 'only methods'









	
