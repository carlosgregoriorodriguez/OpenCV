import cv2
import numpy as np
from time import clock


def integralValue(binImg):
	rawContours,hierarchy = cv2.findContours(binImg.copy(),
		cv2.cv.CV_RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	return cv2.contourArea(rawContours[0])

def transform(windowX,windowY,originalShape,windowShape):
	realX = int(windowX*originalShape[1]/windowShape[0])
	realY = int(windowY*originalShape[0]/windowShape[1])
	return realX,realY

#applies a threshold such that if x is in interval=[a,b] then x remains, else x :=0.
#a and b are included and [a,b] is in [0,infinit]
#for setting interval=[a,infinit] set b=-1
def intervalThreshold(img,interval):
	img = cv2.threshold(img,interval[0]-1,255,cv2.cv.CV_THRESH_TOZERO)[1]
	if interval != -1:
		img = cv2.threshold(img,interval[1],255,cv2.cv.CV_THRESH_TOZERO_INV)[1]
	return img


def greyValueSegmentation(img,segNum):
	aux = cv2.minMaxLoc(img)
	step = int((aux[1]-aux[0])/segNum)
	segMask = np.zeros(img.shape,np.uint8)
	retList = []
	imageList = []
	for i in range(segNum):
		if i==segNum-1:
			valRange = (int(aux[0]+i*step),-1)
		else:	
			valRange = (int(aux[0]+i*step),int(aux[0]+(i+1)*step))
		auxMask = intervalThreshold(img,valRange)
		auxMask = cv2.threshold(auxMask,1,valRange[1],cv2.cv.CV_THRESH_BINARY)[1]
		
		rawContours,hierarchy = cv2.findContours(auxMask.copy(),
		cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		bigCont = []
		if len(rawContours)>0:
			for cnt in zip(hierarchy[0],rawContours):
				#contornos que (no tengan hijos o tengan hermano izquierdo) y no sean unipuntuales
				#print cnt[0]
				#if (cnt[0][2]<0 or cnt[0][0]>-1) and len(cnt[1])>1:
				if len(cnt[1])>1:
					bigCont.append(cv2.approxPolyDP(cnt[1],3,True))
		retList.append(bigCont)
		imageList.append(auxMask)
		segMask = cv2.max(segMask,auxMask)
	return segMask,retList,imageList


def labelConnectedComponents(img):
	print '-LCC-'
	upBond = 100
	mask = np.clip(img,0,1)+upBond
	retList = cv2.minMaxLoc(mask)
	seedVal,seed = int(retList[1]),retList[3]
	auxMask = np.zeros((img.shape[0]+2,img.shape[1]+2),np.uint8)
	compVal = 1
	while (seedVal>upBond):
		cv2.floodFill(mask, auxMask, seed, [compVal,]*3, [0,]*3, [0,]*3, cv2.cv.CV_FLOODFILL_FIXED_RANGE)
		compVal += 1
		retList = cv2.minMaxLoc(mask)
		seedVal,seed = int(retList[1]),retList[3]
		
	aux = np.zeros(mask.shape,np.uint8)
	aux[:,:]=mask
	mask = cv2.threshold(aux,upBond-1,0,cv2.cv.CV_THRESH_TOZERO_INV)[1]
	return mask



def getComponentOf(img,point,nonTrivial):
	print '-COF-'
	myTime = clock()
	mask = np.clip(img,0,1)
	rows,cols = mask.shape[:2]
	rawContours,hierarchy = cv2.findContours(mask.copy(),
		cv2.cv.CV_RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	if len(rawContours)>0:
		distance = []
		for cont in rawContours:
			aux = cv2.pointPolygonTest(cont, point, True)
			if aux >= 0:
				retMask = np.zeros(img.shape,np.uint8)
				cv2.drawContours(retMask,[cont],-1,(1,1,1),-1)
				return retMask
			else:
				distance.append(aux)
		retMask = np.zeros(img.shape,np.uint8)
		cv2.drawContours(retMask,rawContours,distance.index(max(distance)),(1,1,1),-1)
		return retMask
	else:
		retMask = np.zeros(img.shape,np.uint8)
		return retMask
		

if __name__ == "__main__":
	print 'only methods'