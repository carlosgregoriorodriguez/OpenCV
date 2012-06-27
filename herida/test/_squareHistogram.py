import cv2
import numpy as np
from _utils import *

#computes a Sqare histogram for the contours
def getSqHistogram(contours,imgShape,sqNum):
	#compute the width and height of a square
	lh = imgShape[0]/sqNum[0]
	lw = imgShape[1]/sqNum[1]
	
	sqHist = np.zeros(sqNum,np.uint8) #create an appropiate histogram (2D)
	for cont in contours:	#for every contour, we update the histogram
		center,r = cv2.minEnclosingCircle(cont) #take the minimal enclosing circle for the contour
		x,y = int(center[0]),int(center[1])
		r = int(r)
		
		xSq = min(x/lw,sqNum[1]-1)
		ySq = min(y/lh,sqNum[0]-1)


		#compute cardinal points for the center with distance r
		northSq = max((y-r)/lh,0)
		southSq = min((y+r)/lh,sqNum[0])
		
		westSq = max((x-r)/lw,0)
		eastSq = min((x+r)/lw,sqNum[1])
		
		if northSq != southSq:
			for i in range(northSq,min(southSq+1,sqNum[0])):
				if eastSq != westSq:
					for j in range(westSq,min(eastSq+1,sqNum[1])):
						sqHist[i][j]+=1
				else:
					sqHist[i][xSq]+=1
		else:
			if eastSq != westSq:
				for j in range(westSq,min(eastSq+1,sqNum[1])):
					sqHist[ySq][j]+=1
			else:
				sqHist[ySq][xSq]+=1

	return sqHist


#paints the square histogram on a blanck canvas
def paintSqHistogram(sqHist,imgShape,gradual):
	totalH,totalW = imgShape[0],imgShape[1]
	rowNum,colNum = sqHist.shape[:2]
	lh,lw = totalH/rowNum,totalW/colNum

	canvas = np.zeros((totalH,totalW),np.uint8)
	
	#paint the result
	for row in range(rowNum):
		for col in range(colNum):
			if sqHist[row][col]!=0:
				if gradual:
					plane = np.ones((lh,lw),np.uint8)*(120+20*sqHist[row][col])
				else:
					plane = np.ones((lh,lw),np.uint8)*255
				canvas[row*lh:(row+1)*lh,col*lw:(col+1)*lw]=plane	
	
	return canvas


#Removes noise from a square histogram
def removeNotConnected(sqHist):
	for row in range(sqHist.shape[0]-1):
		for col in range(sqHist.shape[1]-1):
			if (sqHist[row,col]!=0) and (not isConnected(row,col,sqHist)):
				sqHist[row,col]=0


def isConnected(row,col,matrix):
	leftB = max(0,col-1)
	rightB = min(col+1,matrix.shape[1]-1)
	upB = max(0,row-1)
	downB = min(row+1,matrix.shape[0]-1)
	for i in range(upB,downB+1,1):
		for j in range(leftB,rightB+1,1):
			if (i!=row or j!=col) and (matrix[i,j]!=0):
				return True
	return False


#Container methods, called from outside
def significantSQS(bigCont,imgShape,histDim):
	sqHist = getSqHistogram(bigCont,(imgShape[0],imgShape[1]),histDim)
	removeNotConnected(sqHist) #not connected is considered noise
	return sqHist



def getSigSquares(contList,imgShape,histDim,thresh):
	print 'in getSigSquares'
	#create a blank canvas to buffer the sum of the sqHists of all elements of the list
	sumSq = np.zeros(histDim,np.uint8)
	#for each list of contours get the sqHist, clip it to [0,1] (convert it to binary image)
	#and add it to the blank canvas
	for contours in contList:
		sqHist = significantSQS(contours,imgShape,histDim)
		np.clip(sqHist,0,1,sqHist)
		sumSq = sumSq+sqHist
	#threshold entries, i.e. consider entries that appear in more than 'thresh' sqHist
	sumSq = cv2.threshold(sumSq,thresh,200,cv2.cv.CV_THRESH_BINARY)[1]
	#remove not connected single entries, again, noise
	removeNotConnected(sumSq)
	#label the connected components in sumSq
	#then get the component that is closer to the center of the image and remove the rest of them
	#sumSq = getCenterComponent(sumSq)
	sumSq = getComponentOf(sumSq,(sumSq.shape[1]/2,sumSq.shape[0]/2),True)
	
	return paintSqHistogram(sumSq,imgShape,False),sumSq


if __name__ == "__main__":

	print 'only methods'































