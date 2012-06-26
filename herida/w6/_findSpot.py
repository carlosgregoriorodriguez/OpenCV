import cv2
import numpy as np
from _utils import *
from _fleshBackProyection import *


#def segmentImg(img,mask,...):
# segmentamos la imagen en una escala de grises fina con greyValueSegmentation.
# segun nos vamos moviendo se van iluminando las zonas con verde.
# si el usuario mueve el raton sobre un contorno verde, se aisla y se guarda.
# hay una opcion para mostrar todos los contornos.
# hay una opcion para elegir el canal que se quiere segmentar
# hay una opcion para elegir el tamanio de los intervalos 

# #idea 2:
# quitar los valores altos de la imagen, para poder multiplicar y agrandar la diferencia
# para los valores altos, hacer una matriz auxiliar que sea np.array(matriz anterior,np.int32)

def findSpotsInRed(original,mask,levelNumber,level):

	redChannel = cv2.min(mask,cv2.split(original)[0])
		
	if redChannel.shape[0]>1000 or redChannel.shape[1]>1000:
		aux = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
	elif redChannel.shape[0]>500 or redChannel.shape[1]>500:
		aux = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
	else:
		aux = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
	
	redChannelBF = cv2.morphologyEx(redChannel, cv2.MORPH_OPEN,aux)
	
	#redChannel,contByLvl,imageList = greyValueSegmentation(redChannelBF,levelNumber)
	#redChannel = cv2.merge([np.clip(imageList[level],0,1)*255,]*3)
	
	redChannelBF = scaleImgValuesClip(redChannelBF,240)
	kernel = np.ones((3,3),np.uint8)*255
	redChannelBF = cv2.erode(redChannelBF.copy(),kernel,iterations=3,borderType=cv2.BORDER_CONSTANT,borderValue=0)

	redChannelBF,contByLvl,imageList = greyValueSegmentation(redChannelBF,levelNumber)

	# rawContours,hierarchy = cv2.findContours(redChannel.copy(),
	# 	cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	# bigCont = []
	# if len(rawContours)>0:
	# 	for cnt in zip(hierarchy[0],rawContours):
	# 		if len(cnt[1])>1:
	# 			bigCont.append(cv2.approxPolyDP(cnt[1],3,True))
	

	# rawContours,hierarchy = cv2.findContours(redChannelBF.copy(),
	# 	cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	# bigContMedia = []
	# if len(rawContours)>0:
	# 	for cnt in zip(hierarchy[0],rawContours):
	# 		if len(cnt[1])>1:
	# 			bigContMedia.append(cv2.approxPolyDP(cnt[1],3,True))
	

	
	
	if len(contByLvl)>0:
		points = getPoints(contByLvl)
		retImg = np.zeros(redChannel.shape,np.uint8)
		mask = np.zeros((redChannel.shape[0]+2,redChannel.shape[1]+2),np.uint8)
		for seedPoint in points:
			aux = redChannel.copy()
			cv2.floodFill(aux, mask, seedPoint, [255,]*3, [3,]*3, [3,]*3)
			aux = cv2.threshold(aux,254,255,cv2.cv.CV_THRESH_BINARY)[1]
			retImg = retImg+aux

	redChannel = cv2.merge([redChannel,]*3)
	retImg = cv2.merge([retImg,]*3)
	#aux = redChannel.copy()

	#markers = np.array(makeMarkers(redChannelBF,15),np.int32)
	#cv2.watershed(original, markers)
	#redChannelBF = cv2.merge([redChannelBF,]*3)

	#cv2.drawContours(redChannel,bigCont,-1,(0,255,0),2)

	#cv2.drawContours(redChannelBF,bigContMedia,-1,(0,255,0),2)

	#redChannel = cv2.merge([redChannel,]*3)
	
	#cv2.drawContours(redChannel,contByLvl[level],-1,(0,255,0),2)
	
	#return original

	edges = cv2.Canny(cv2.split(redChannelBF)[0], 500, 50) #,L2gradient=True)
	edges = cv2.merge([edges,]*3)

	return redChannel,edges


	







def getContoursInFlesh(img,mask):
	print '-FINDSPOT-getContours'

	rawContours,hierarchy = cv2.findContours(mask.copy(),
		cv2.cv.CV_RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

	print '-FINDSPOT-rawContour'
	#print rawContours
	print '-FINDSPOT-hierarchy'
	print hierarchy
	print len(rawContours)
	bigCont = [] #contours with more than one element
	for cnt in zip(hierarchy[0],rawContours):
		#print cnt
		#todos los contornos que no tengan hijos (cnt[0][2]<0) y tengan padre (cnt[0][3]>-1)
		if cnt[0][2]<0 and cnt[0][3]>-1:
			if len(cnt[1])>1:
				cvxH = cv2.convexHull(cnt[1])
				area = cv2.contourArea(cvxH,False)
				if area>5:
					bigCont.append(cvxH)
	print bigCont
	return bigCont

def getHistRGB(img,mask):
	imgArray = [img,]
	channels = [0,1]
	histSize = [128,128]
	ranges = [0,256,0,256]
	hist = cv2.calcHist(imgArray,channels,mask,histSize,ranges) 
	aux = cv2.calcBackProject(imgArray,[0,1], hist, [0,256,0,256],1)
	return aux


def markColors(probMask):
	canvas = np.zeros((probMask.shape[0],probMask.shape[1],3),np.uint8)
	maxVal = cv2.minMaxLoc(probMask)[1]
	step = 40

	for i in range(0,int(maxVal/step)):
		if i == int(maxVal/step)-1:
			interval = (i*step,maxVal)
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*maxVal
			
		else:
			interval = (i*step,(i+1)*step)
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*i*step
	
		layer = cv2.merge([layer,]*3)
		canvas[:,:,:]=canvas[:,:,:]+layer
	return canvas


def identifyLevels(probMask):
	canvas = np.zeros((probMask.shape[0],probMask.shape[1],3),np.uint8)
	maxVal = cv2.minMaxLoc(probMask)[1]
	step = int(maxVal/5)

	for i in range(5):
		interval = (i*step,(i+1)*step)
		if i == 0:
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*50
			layer = cv2.merge([layer,]*3)
			canvas[:,:,:]=canvas[:,:,:]+layer
		elif i == 4:
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*255
			layer = cv2.merge([layer,]*3)
			canvas[:,:,:]=canvas[:,:,:]+layer
		else:
			layer = np.clip(intervalThreshold(probMask.copy(),interval),0,1)*255
			canvas[:,:,i-1]=canvas[:,:,i-1]+layer

	return canvas


def findColorMarks(img,mask):
	cuttedImg = cv2.merge([cv2.min(mask,layer) for layer in cv2.split(img)])
	print '-FINDSPOT-findColorMarks'
	cuttedImgBP = getHistRGB(cuttedImg,mask)
	cuttedImgBP = cv2.min(cuttedImgBP,mask)
	#return cv2.merge([cuttedImgBP,]*3)
	return identifyLevels(cuttedImgBP)




if __name__ == "__main__":

	print 'only methods'































