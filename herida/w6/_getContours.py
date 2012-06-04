import cv2
import numpy as np
import math

#get the contours in the image that validate the given parameters
def stapleCont(img,dirList):	
	minArea = dirList[0]
	maxArea = dirList[1]
	direction = dirList[2]

	if minArea>maxArea:
		minArea,maxArea=maxArea,minArea

	rawContours,hierarchy = cv2.findContours(img.copy(),
		cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	bigCont = [] #contours with more than one element
	for cnt in rawContours:
		if len(cnt)>1:
			cvxH = cv2.convexHull(cnt)
			area = cv2.contourArea(cvxH,False)
			if (area>minArea and area<maxArea):
				bigCont.append(cvxH)
		
	bigCont = sortByDirection(bigCont,direction)

	return bigCont


# selects the contours with a given direction space in degrees
# 0->between 0 and 45 degrees
# 1->between 45 and 90 deg
# 2->between 90 and 135 deg
# 3->between 135 and 180 deg
# 4->computes all directions 
#	 gets the maximal direction space
#	 and returns the contours with their
#	 direction in this direction space 
# 5->all directions

def sortByDirection(contours,direction):
	
	if direction not in range(6):
		direction = 5

	if direction!=5:
		#get the direction vector for every contour
		
		directionHist = [0,]*4	
		contByDirection = [[],[],[],[]]

		i = 1
		for cont in contours:
			l = cv2.fitLine(cont, cv2.cv.CV_DIST_L2, 0, 0.1, 0.1)
			v = (l[0],l[1])
			index = getDirectionArea(v)
			contByDirection[index].append(cont)
			if i:
				i = 0	
			directionHist[index]+=1

		if direction==4: 
			return contByDirection[directionHist.index(max(directionHist))]
		else:
			return contByDirection[direction]
	return contours
		

def getDirectionArea(v):
	if math.degrees(math.asin(abs(v[1])))<45:
		if ((v[0]>0 and v[1]<=0) or (v[0]<0 and v[1]>=0)) :
			return 0
		else:
			return 3
	else:
		if ((v[0]>=0 and v[1]<0) or (v[0]<=0 and v[1]>0)) :
			return 1
		else:
			return 2




if __name__ == "__main__":
	print 'only methods'












