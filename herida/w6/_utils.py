import cv2
import numpy as np
from time import clock

#applies a threshold such that if x is in interval=[a,b] then x remains, else x :=0.
#a and b are included and [a,b] is in [0,infinit]
#for setting interval=[a,infinit] set b=-1
def intervalThreshold(img,interval):
	img = cv2.threshold(img,interval[0]-1,255,cv2.cv.CV_THRESH_TOZERO)[1]
	if interval != -1:
		img = cv2.threshold(img,interval[1],255,cv2.cv.CV_THRESH_TOZERO_INV)[1]
	return img

def scaleImgValues(img):
	maxVal = cv2.minMaxLoc(img)[1]

	if maxVal>0:
		print 'values '+str(cv2.minMaxLoc(img))
		print 'coef '+str(256/maxVal)+' highest value '+str(maxVal*(256/maxVal))
		aux = np.array((255/maxVal)*1.1*img,np.float)
		img = np.array(np.clip(aux,0,255),np.uint8)
		print 'max value as numpy array '+str(img.max())
		print 'new values '+str(cv2.minMaxLoc(img))
	return img

def scaleImgValuesClip(img,scale):
	
	img = np.clip(img,0,scale)
	maxVal = cv2.minMaxLoc(img)[1]

	if maxVal>0:
		print 'values '+str(cv2.minMaxLoc(img))
		print 'coef '+str(255/maxVal)+' highest value '+str(maxVal*(255/maxVal))
		aux = np.array((255/maxVal)*1.1*img,np.float)
		img = np.array(np.clip(aux,0,255),np.uint8)
		print 'max value as numpy array '+str(img.max())
		print 'new values '+str(cv2.minMaxLoc(img))
	return img


def greyValueSegmentation(img,segNum):
	aux = cv2.minMaxLoc(img)
	step = int((aux[1]-aux[0])/segNum)
	segMask = np.zeros(img.shape,np.uint8)
	retList = []
	imageList = []
	for i in range(segNum):
		if i==segNum-1:
			print 'HIGHEST VALUE'
			valRange = (int(aux[0]+i*step),-1)
			auxMask = intervalThreshold(img,valRange)
			auxMask = cv2.threshold(auxMask,1,255,cv2.cv.CV_THRESH_BINARY)[1]
		else:	
			valRange = (int(aux[0]+i*step),int(aux[0]+(i+1)*step))
			auxMask = intervalThreshold(img,valRange)
			auxMask = cv2.threshold(auxMask,1,valRange[1],cv2.cv.CV_THRESH_BINARY)[1]
		


		rawContours,hierarchy = cv2.findContours(auxMask.copy(),
		cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		bigCont = []
		if len(rawContours)>0:
			for cnt in zip(hierarchy[0],rawContours):
				if len(cnt[1])>1:
					bigCont.append(cv2.approxPolyDP(cnt[1],3,True))
		retList.append(bigCont)
		imageList.append(auxMask)
		segMask = cv2.max(segMask,auxMask)
	return segMask,retList,imageList


def getPointsInContours(contours):
	retList = []
	for cont in contours:
		retList.append(cv2.minEnclosingCircle(cont)[0])
	return retList

def getPoints(contoursList):
	retList = []
	for contours in contoursList:
		retList = retList + getPointsInContours(contours)
	return retList



def makeMarkers(img,segNum):
	aux = cv2.minMaxLoc(img)
	step = int((aux[1]-aux[0])/segNum)
	segMask = np.zeros(img.shape,np.uint8)
	for i in range(segNum):
		if i==segNum-1:
			print 'HIGHEST VALUE'
			valRange = (int(aux[0]+i*step),-1)
			auxMask = intervalThreshold(img,valRange)
			auxMask = cv2.threshold(auxMask,1,i+1,cv2.cv.CV_THRESH_BINARY)[1]
		else:	
			valRange = (int(aux[0]+i*step),int(aux[0]+(i+1)*step))
			auxMask = intervalThreshold(img,valRange)
			auxMask = cv2.threshold(auxMask,1,i+1,cv2.cv.CV_THRESH_BINARY)[1]
		
		segMask = cv2.max(segMask,auxMask)
	return segMask






def labelConnectedComponents(img):
	print '-LCC-'
	upBond = 100
	mask = np.clip(img,0,1)+upBond
	# print mask
	retList = cv2.minMaxLoc(mask)
	seedVal,seed = int(retList[1]),retList[3]
	auxMask = np.zeros((img.shape[0]+2,img.shape[1]+2),np.uint8)
	compVal = 1
	# print 'before while'
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
		

#returns a binary image with 1 for the conected component nearest to the point and 0 the rest
#point in normal format, point=(column,row)
# def getComponentOf(img,point,nonTrivial):
# 	print '-COF-'
# 	#print '-COF-labelConnectedComponent'
# 	myTime = clock()
# 	mask = np.clip(img,0,1)
# 	print '-COF-mask'+str(type(mask))
# 	print mask
# 	#print '-COF- ===>takes '+str(clock()-myTime)
# 	rows,cols = mask.shape[:2]
# 	pr,pc = point[1],point[0] #pr is point row, pc is point column
# 	#print pr
# 	#print pc
# 	label = 0
# 	labelPoint = point
# 	#if the point is in the image
# 	if(pr>=0 and pr<rows and pc>=0 and pc<cols):
# 		#print 'in first if'
# 		#get the label of the point
# 		label = mask[pr][pc]
# 		#if the nearest non trivial componen is asked (trivial = label 0)
# 		#and the matrix has non zero elements
# 		#and the point is in the trivial component (component with label 0)
# 		print '-COF- before if with data:'
# 		print 'label '+str(label)+' nonTrivial '+str(nonTrivial)+' maxValue '+str(cv2.minMaxLoc(mask)[1])

# 		if nonTrivial and cv2.minMaxLoc(mask)[1]>0 and label==0:
# 			print 'in second if'
# 			dist = 0
# 			#while the label is 0 compute a square of increasing dimension centered on the point
# 			#and look for the maximum
# 			while label == 0:
# 				#increase the distance
# 				dist += 1
# 				print 'in while'
# 				print 'label '+str(label)
# 				print 'dist '+str(dist)

# 				#get the square of distance dist and centered on the point
# 				distRect = mask[max(0,pr-dist):min(rows,pr+dist),max(0,pc-dist):min(cols,pc+dist)]
# 				#the nearest label will be the first component that appears in this increasing square
# 				auxList = cv2.minMaxLoc(distRect)
# 				label = auxList[1]
# 				labelPoint = (auxList[3][0]+pc-dist,auxList[3][1]+pr-dist)
# 				print labelPoint
# 				print 'distRect shape = '+str(distRect.shape)
# 				print 'mask shape = '+str(mask.shape)
# 				#if the increasing square reaches the dimension of the whole image break
# 				if (distRect.shape[0]==rows and distRect.shape[1]==cols):
# 					break
# 		auxMask = np.zeros((mask.shape[0]+2,mask.shape[1]+2),np.uint8)
# 		print '-COF- before floodFill with parameters:'
# 		print '-COF- mask shape: '+str(mask.shape)
# 		print 'labelPoint: '+str(labelPoint)
# 		print mask[labelPoint[1]-5:labelPoint[1]+5,labelPoint[0]-5:labelPoint[0]+5]
# 		cv2.floodFill(mask, auxMask, labelPoint, [255,]*3, [0,]*3, [0,]*3, cv2.cv.CV_FLOODFILL_FIXED_RANGE)
# 		print mask[labelPoint[1]-5:labelPoint[1]+5,labelPoint[0]-5:labelPoint[0]+5]
# 		mask = cv2.threshold(mask,200,1,cv2.cv.CV_THRESH_BINARY)[1]	
# 		print mask[labelPoint[1]-5:labelPoint[1]+5,labelPoint[0]-5:labelPoint[0]+5]
# 	return mask	


#returns a binary image with 1 for the conected component nearest to the point and 0 the rest
#point in matrix format, point=(row,column)
# def getComponentOf(img,point,nonTrivial):
# 	print '-COF-'
# 	print '-COF-labelConnectedComponent'
# 	myTime = clock()
# 	mask = labelConnectedComponents(img)
# 	print '-COF- ===>takes '+str(clock()-myTime)
# 	rows,cols = mask.shape[:2]
# 	pr,pc = point[0],point[1] #pr is point row, pc is point column
# 	#print pr
# 	#print pc
# 	label = 0
# 	#if the point is in the image
# 	if(pr>=0 and pr<rows and pc>=0 and pc<cols):
# 		#print 'in first if'
# 		#get the label of the point
# 		label = mask[pr][pc]
# 		#if the nearest non trivial componen is asked (trivial = label 0)
# 		#and the matrix has non zero elements
# 		#and the point is in the trivial component (component with label 0)
# 		if nonTrivial and cv2.minMaxLoc(mask)>0 and label==0:
# 			#print 'in second if'
# 			dist = 0
# 			#while the label is 0 compute a square of increasing dimension centered on the point
# 			#and look for the maximum
# 			while label == 0:
# 				print 'in while'
# 				print 'label '+str(label)
# 				print 'dist '+str(dist)

# 				#increase the distance
# 				dist += 1
# 				#get the square of distance dist and centered on the point
# 				distRect = mask[max(0,pr-dist):min(rows,pr+dist),max(0,pc-dist):min(cols,pc+dist)]
# 				#the nearest label will be the first component that appears in this increasing square
# 				label = cv2.minMaxLoc(distRect)[1]
# 				print 'distRect shape = '+str(distRect.shape)
# 				print 'mask shape = '+str(mask.shape)
# 				#if the increasing square reaches the dimension of the whole image break
# 				if (distRect.shape[0]==rows and distRect.shape[1]==cols):
# 					break
# 		elif (not nonTrivial) and label==0:
# 			#negMask has 1 where mask has 0 and 0 where mask has 1 or more
# 			negMask = np.ones((rows,cols),np.uint8)-np.clip(mask,0,1) #negMask has 1 where mask
# 			# print 'out of getComponent'
# 			# print negMask
# 			return getComponentOf(negMask,point,False) #now point is in a non trivial component
	
# 	aux = np.zeros((mask.shape),np.uint8)
# 	aux[:,:]=mask
# 	mask = intervalThreshold(aux,(label,label))
# 	np.clip(mask,0,1)
# 	#print 'out of getComponent2'
# 	return mask	



#hacer esto con floodfill:
#busca maximo con minmaxloc
#hace clip a [0,1]
#hace floodfill con la posicion del maximo y lo pone a -1
#busca sucesivos maximos para hacer floodfill en ellos con -i donde i es la iteracion del bucle
#luego multiplica por -1 toda la matriz
#
#PASARLO A _UTILS!!

# def labelConectComp(sqHist):
#  	#print sqHist
 	
#  	#put all positive entries to negative
#  	sqHist= sqHist*(-1)
#  	#print sqHist
 	
#  	#create the current label variable
#  	label = 0
 	
#  	#move through all sqHist
#  	for row in range(sqHist.shape[0]):
#  		for col in range(sqHist.shape[1]):
#  			#if the entry at row,col is relevant and not labeled yet
#  			if sqHist[row][col]<0:
 				
#  				#update label
#  				label+=1
#  				#print 'going to label '+str((row,col))+' with label '+str(label)
#  				#put all entries neighboured with the current entry to the same label
#  				aux = set()
#  				getComponent((row,col),sqHist,aux,False)
#  				for tile in aux:
#  					sqHist[tile[0]][tile[1]]=label
#  	return sqHist	

if __name__ == "__main__":
	print 'only methods'