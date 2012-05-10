import cv2
import numpy as np
import sys
from glob import glob



def dummy(x):
	print x


def getHistogram(img):
	h = np.zeros((256,256,3));
	b,g,r = img[:,:,0],img[:,:,1],img[:,:,2]
	bins = np.arange(257)
	bin = bins[0:-1]
	color = [ (255,0,0),(0,255,0),(0,0,255) ]
	for item,col in zip([b,g,r],color):

		#NORMALIZAR EL HISTOGRAMA
		N,bins = np.histogram(item,bins)
		v=N.max()
		bins=cv2.normalize(bins,bins,1,255,cv2.NORM_MINMAX)
		N = np.int32(np.around((N*255)/v))
		N=N.reshape(256,1)
		pts = np.column_stack((bin,N))
		cv2.polylines(h,np.array([pts],np.int32),False,col,1)
	h=np.flipud(h)
	return h





if __name__ == "__main__":
	
	path = '../images/contourOnly/*.jpg'
	imageNames = glob(path)
	imgIndex = 0
	img = cv2.imread(imageNames[imgIndex])
	showImg = img.copy()

	cv2.namedWindow('image',cv2.cv.CV_WINDOW_AUTOSIZE)

	canvas = np.zeros((476,266,3),np.uint8)
	

	history = []

	# method for the mouse event
	def onmouse(event, x, y, flags, param):
		showImg[:,:,:] = img
		center = (x,y)
		pt1 = (x-50,y-50)
		pt2 = (x+50,y+50)
		cv2.rectangle(showImg, pt1, pt2, (0,0,255), thickness=3)
		patch = cv2.pyrUp(cv2.getRectSubPix(img, (100,100), center))
		canvas[0:200,0:200,:]=patch
		canvas[210:466,0:256,:]=getHistogram(patch)
		if flags & cv2.EVENT_FLAG_LBUTTON:
			history.append(canvas.copy())


	def showHistory(history):
		l = len(history)
		if l>0:
			historyCanvas = np.zeros((476,((l/2)+1)*266,3), np.uint8)
			for elem in enumerate(history):
				if elem[0]%2:
					historyCanvas[0:476,elem[0]/2*266:(elem[0]/2+1)*266,:]=elem[1]
		else:
			historyCanvas = np.zeros((50,50,3), np.uint8)


		return historyCanvas



	cv2.setMouseCallback('image', onmouse)
	
	while True:	

		cv2.imshow('image',showImg)
		cv2.imshow('zoom and histogram',canvas)
		historyCanvas = showHistory(history)
		cv2.imshow('historyCanvas',historyCanvas)
		
		key = cv2.waitKey(5)
	 	if (key==120):
	 		imgIndex = (imgIndex+1,imgIndex)[imgIndex==(len(imageNames)-1)]
	 		img = cv2.imread(imageNames[imgIndex])
	 		showImg=img.copy()
	 	elif (key==122):
	 		imgIndex = (imgIndex-1,imgIndex)[imgIndex==0]
	 		img = cv2.imread(imageNames[imgIndex])
	 		showImg=img.copy()
	 	elif (key != -1):
	 		break


