import numpy as np
import cv2

def erode(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		erosion = cv2.erode(img,kernel,iterations = 1)
		return erosion
def closeContour(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		closeResult = cv2.morphologyEx(img,cv2.MORPH_OPEN, kernel)
		return closeResult

def dilate(img, kernelSize=5):
		kernel = np.ones((kernelSize,kernelSize),np.uint8)
		dilateResult = cv2.dilate(img,kernel,iterations = 1)
		return dilateResult

imOrig = cv2.imread('test7.png')
numControl = 10
nContour = 0
lastContours = 0
contours = []
while ((2*lastContours>=nContour) and numControl>0):
	im = dilate(closeContour(imOrig, numControl-1),(numControl+1)/2)
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,200,255,0)
	im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	lastContours = nContour		
	nContour = len(contours)
	if (lastContours == 0):#caso 0
		lastContours = nContour	
	numControl=numControl-1
	print "numControl = "+str(numControl)+" lastContours = "+str(lastContours)+" nContours = "+str(nContour)

area = np.zeros(len(contours))
index = 0
for cnt in contours:
	area[index] = cv2.contourArea(cnt)
	#print area[index]
	index=index+1
meanArea = np.mean(area)
print "Area media: "+str(meanArea)
#eliminamos los que estan por debajo de 0.5 veces el area media (quitamos ruido)
toDelete = np.where(area<=.5* meanArea)
goodContours = np.delete(contours, toDelete)
#calculamos ajuste a elipse:

cv2.drawContours(im, goodContours, -1, (0,0,255), 1) 
cv2.imshow("Original", im)
cv2.waitKey(0)