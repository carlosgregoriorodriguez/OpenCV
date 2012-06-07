import cv2
import numpy as np
from _utils import *

#computes a Sqare histogram for the contours
def getSqHistogram(contours,imgShape,sqNum):
	#compute the width and height of a square
	lh = imgShape[0]/sqNum[0]
	lw = imgShape[1]/sqNum[1]
	
	#print "lw "+str(lw)+" imgShape[0] "+str(imgShape[1])+" sqNum "+str(sqNum[1])
	#print "lh "+str(lh)+" imgShape[1] "+str(imgShape[0])+" sqNum "+str(sqNum[0])

	sqHist = np.zeros(sqNum,np.uint8) #create an appropiate histogram (2D)
	for cont in contours:	#for every contour, we update the histogram
		#print "new contour"
		center,r = cv2.minEnclosingCircle(cont) #take the minimal enclosing circle for the contour
		x,y = int(center[0]),int(center[1])
		r = int(r)
		
		#print "center "+str((x,y))+" radius "+str(r)

		xSq = min(x/lw,sqNum[1]-1)
		ySq = min(y/lh,sqNum[0]-1)


		#compute cardinal points for the center with distance r
		northSq = max((y-r)/lh,0)
		southSq = min((y+r)/lh,sqNum[0])
		
		westSq = max((x-r)/lw,0)
		eastSq = min((x+r)/lw,sqNum[1])
		

		#print "center row at "+str(ySq)+" up to "+str(northSq)+" down to "+str(southSq)
		#print "center col at "+str(xSq)+" left to "+str(westSq)+" right to "+str(eastSq)
		
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
	sumSq = getComponentOf(sumSq,(sumSq.shape[0]/2,sumSq.shape[1]/2),True)

	return paintSqHistogram(sumSq,imgShape,False),sumSq


def getComponent(entry,sqHist,neig,diagonalNeig):
	row = entry[0]
	col = entry[1]
	if row>=0 and row<sqHist.shape[0] and col>=0 and col<sqHist.shape[1] and sqHist[row][col]<0 and entry not in neig:
		neig.add(entry)
		neig.update(getComponent((row-1,col),sqHist,neig,diagonalNeig))
		neig.update(getComponent((row+1,col),sqHist,neig,diagonalNeig))
		neig.update(getComponent((row,col-1),sqHist,neig,diagonalNeig))
		neig.update(getComponent((row,col+1),sqHist,neig,diagonalNeig))
	return neig



#gets the component containing the center pixel or the nearest component to this pixel
def getCenterComponent(sqHist):
	sqHist = labelConnectedComponents(sqHist)
	rows,cols = sqHist.shape[:2]
	centerLabel = sqHist[rows/2][cols/2]
	dist = 0
	if cv2.minMaxLoc(sqHist)[1]!=0:
		while centerLabel == 0:
			dist += 1
			distRect = sqHist[max(0,rows/2-dist):min(rows-1,rows/2+dist),max(0,cols/2-dist):min(cols-1,cols/2+dist)]
			centerLabel = cv2.minMaxLoc(distRect)[1]
			if (distRect.shape[0]==rows and distRect.shape[1]==cols):
				break

	aux =np.zeros((sqHist.shape),np.uint8)
	aux[:,:]=sqHist
	sqHist = intervalThreshold(aux,(centerLabel,centerLabel))
	return sqHist




#not used yet
def getPoints(imgShape,sqHist):
	retPoints = []

	rowNum,colNum = sqHist.shape[:2]
	lw = imgShape[1]/colNum
	lh = imgShape[0]/rowNum

	for row in range(rowNum):
		for col in range(colNum):
			if sqHist[row][col]!=0:
				x,y = col*lw,row*lh
				aux = []
				for i in range(3):
					for j in range(3):
						aux.append((x+(lw/2)*i,y+(lh/2)*j))
				retPoints.append(aux)
	return retPoints


#tests if a point is in a contour
def isContained(pt,contours):
 	for cont in contours:
 		if cv2.pointPolygonTest(cont, pt, False)>=0:
 			return True
 	return False

if __name__ == "__main__":

	print 'only methods'































