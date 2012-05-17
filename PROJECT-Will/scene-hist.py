#               PROJECT - Video Analysis
#    Press SPACE to capture frame 
#
#    Press 'P' to pause video. To resume press any key
#    Press 'F' to make video faster
#    Press 'S' to make video go slower
#    Press 'R' to clear Histograms window
#
#    Willie - week 4 a.P. (after Project)


import cv2
import cv2.cv as cv
import time
import numpy as np
import random as rd

debugging = True   # Boolean variable for debugging

bins = np.arange(256).reshape(256,1)

method_dict = ['CORRELATION' , 'CHISQUARE' , 'INTERSECT', 'BHATTACHARYYA' ]

usage = '''
USAGE:      SPACE - capture frame

            'P' - to pause. To resume press any key

            'F' - makes video run faster

            'S' - makes video run slower

     QUIT: press either q or ESC
'''

def dummy(p):
	print "compare histogram method changed to "+method_dict[p]


def getHistogram(img):

	# First calculate histogram
	histogram = cv2.calcHist([img],[0],None,[256],[0,255]) 
	
	# Normalize obtained histogram	
	cv2.normalize(histogram,histogram,0,255,cv2.NORM_MINMAX)
		
	return histogram


def printHistogram(histogram,canvas,withColor):

	h = np.int32(np.around(histogram))
	pts = np.column_stack((bins,h))
	color = None
	if withColor:
		color = (rd.randint(0,255),rd.randint(0,255),rd.randint(0,255))
	else:
		color = 50

	cv2.polylines(canvas,np.array([pts],np.int32),False,color,2)

	return canvas


def drawString(text, (x, y), img):
	cv2.putText(img, text, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, linetype=cv2.CV_AA)
	cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), linetype=cv2.CV_AA)


def main():

	print usage

	pause = False
	speed = 20

	# Create black image from which to compare the Raw-Substraction
	black = np.zeros((368,480),dtype=np.uint8)
	baseHist = getHistogram(img= black)

	# Load video
	vid = cv2.VideoCapture("videos/FamilyGuy.mp4")

	# Create list in which captured frames are stored
	frames = []
	histResult = np.zeros((300,255,3))

	# Create window
	cv2.namedWindow("Raw-Substraction")
	cv2.createTrackbar("method","Raw-Substraction",0,3,dummy)


	while True: 

		if not pause:
			succesFlag , frameOriginal = vid.read()
			frame = cv2.cvtColor(frameOriginal,cv.CV_RGB2GRAY)

		key = cv2.waitKey(speed)

		if (key == 112):  # press 'P'
			pause = not pause
			if pause:
				print "PAUSE"
			else:
				print "RESUME"

		if (key == 115):  # press 'S'
			speed += 5
			print "speed: "+str(speed)

		if (key == 102):  # press 'F'
			if speed != 5:
				speed -= 5
				print "speed: "+str(speed)

		if (key == 32):   # press SPACE
			n = len(frames)
			print "Frame %d captured"%(n)
			capture = frame.copy()
			frames.append(capture)


			cv2.imshow("frame %d capture"%(n),cv2.pyrDown(capture))
			a = None
			if (n%12 < 6):
				a = 410
			else:
				a = 550
			cv.MoveWindow("frame %d capture"%(n),(n%6)*190 + 50,a)

		
		cv2.imshow("ORIGINAL",frame)
		cv.MoveWindow("ORIGINAL",50,20)

		if (len(frames) > 0):
			#for img in frames:
			frame1 = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(frame)))))

			capture1 = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(capture)))))

			final = cv2.resize(cv2.absdiff(frame1,capture1), (480,368) )

			hh = getHistogram(img= final)

			final = printHistogram(histogram= hh, canvas= final , withColor= False)

			method = cv2.getTrackbarPos("method","Raw-Substraction")

			distance = str(cv2.compareHist(hh,baseHist,method))

			drawString(method_dict[method]+"  "+distance , (20,20),final)

			cv2.imshow("Raw-Substraction",final) 
	
		if debugging:
			cv2.imshow("FAMILY GUY Snippet [ORIGINAL]",cv2.pyrDown(frameOriginal))
			cv.MoveWindow("FAMILY GUY Snippet [ORIGINAL]",800,415)

		if (key == 27 or key == 113):
			print "Quit"
			break



if __name__ == '__main__':
	main()

