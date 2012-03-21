import cv2
import numpy as np
import sys



def dummy(x):
	print x

if __name__ == "__main__":


	print """
		Trackbar mode: 	0 -> CV_RETR_EXTERNAL
						1 -> CV_RETR_LIST
						2 -> CV_RETR_CCOMP
						3 -> CV_RETR_TREE

		Trackbar contour area: sets the minimum area size of a contour to be shown

	"""


	# img is obtained as follows: load image -> converted to gray -> threshold binary(threshold = 128, maxval = 255)
	img = cv2.threshold(cv2.cvtColor(cv2.imread('../../img/stop.jpg'),cv2.cv.CV_RGB2GRAY), 128, 255, cv2.THRESH_BINARY)[1]

	# a black canvas of the size of the image to draw the contours
	canvas = np.zeros((img.shape[0],img.shape[1],3),np.uint8)


	#create a window
	cv2.namedWindow("contour")
    
	#trackbars to select the color for the hulls
	cv2.createTrackbar("r","contour",10,255,dummy)
	cv2.createTrackbar("g","contour",10,255,dummy)
	cv2.createTrackbar("b","contour",10,255,dummy)

	while True:	

		#calculate the contours	
		rawContours,hierarchy = cv2.findContours(img.copy(),cv2.cv.CV_RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

		aux = canvas.copy()
		
		# replace contours with convexHull
		hulls = [cv2.convexHull(cnt) for cnt in rawContours]
		#replace the contours with polynoms
		polynoms = [cv2.approxPolyDP(cnt,3,True) for cnt in rawContours]

		#fill the hulls with the selected color
		cv2.drawContours(aux,hulls,-1,
			(cv2.getTrackbarPos("r","contour"),cv2.getTrackbarPos("g","contour"),cv2.getTrackbarPos("b","contour")),
			cv2.cv.CV_FILLED)
		#paint the polinoms over the hulls
		cv2.drawContours(aux,polynoms,-1,(255,255,255))

		#cv2.imshow("passed img transformed",img)
		cv2.imshow("contour",aux)

		
		if (cv2.waitKey(5)!=-1):
			break


