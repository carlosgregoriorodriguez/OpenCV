import cv2
import numpy as np

def showHist(img,histImg,windowName):
	
	hist_item = cv2.calcHist([img],[0],None,[256],[0,255]) 
		
	cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)

	hist=np.int32(np.around(hist_item))


	pts = np.column_stack((np.arange(256).reshape(256,1),hist))

	cv2.polylines(histImg,np.array([pts],np.int32),False,[255,255,255])
	
	histImg=np.flipud(histImg)

	cv2.imshow(windowName,histImg)




if __name__ == "__main__":

	camera = cv2.VideoCapture(0)


	back = np.zeros((300,255,3))
	


	while True:

		f,img = camera.read()

		img = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)

		eqImg = cv2.equalizeHist(img)

		cv2.imshow("original",img)
		cv2.imshow("eq image",eqImg)

		showHist(img,np.copy(back),"histOriginal")

		showHist(eqImg,np.copy(back),"histEQ")

		if(cv2.waitKey(5)!=-1):
			break





