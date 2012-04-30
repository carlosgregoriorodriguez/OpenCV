#               PROJECT - Video Analysis
#    Press SPACE to capture frame from then on the video will be
#      the raw substraction of the fram capture form the original video
#
#    Press 'R' to reset capture frame
#    Press 'P' to pause video. To resume press any key
#    Press 'B' to toggle between b/w and color video
#    Press 'F' to make video faster
#    Press 'S' to make video go slower
#
#    Willie - week 2 a.P. (after Project)


import cv2
import cv2.cv as cv
import time
import numpy as np

debugging = True   # Boolean variable for debugging

usage = '''
USAGE:      SPACE - capture frame. From then on the video will be the raw
                substraction of the fram capture form the original video

            'R' - reset video.

            'P' - to pause. To resume press any key

            'F' - makes video run faster

            'S' - makes video run slower

            Press 'B' to toggle between b/w and color

     QUIT: press either q or ESC
'''


def dummyX(x):
	print "X-value "+str(x+1)


def dummyY(y):
	print "Y-value "+str(y+1)

def dummyP(p):
	print "Number of pyrUp + pyrDown "+str(p)

def main():

	print usage

	doRS = False
	bw = True
	pause = False
	speed = 10

	vid = cv2.VideoCapture("videos/FamilyGuy.mp4")

	# Create window and trackbars to control smoothing
	cv2.namedWindow("blur")
	cv.MoveWindow("blur",700,50)

	cv2.createTrackbar("ksize.X","blur",0,99,dummyX)
	cv2.createTrackbar("ksize.Y","blur",0,99,dummyY)
	cv2.createTrackbar("number of pyr","blur",0,100,dummyP)

	while True: 

		succesFlag , frameOriginal = vid.read()

		frame = frameOriginal.copy()

		# APPLY SMOOTHING 
		frame = cv2.blur(frame,(cv2.getTrackbarPos("ksize.X","blur")+1,cv2.getTrackbarPos("ksize.Y","blur")+1))

		times = cv2.getTrackbarPos("number of pyr","blur")

		for aux in range(times):
			frame = cv2.pyrDown(frame)
			frame = cv2.pyrUp(frame)

		key = cv2.waitKey(speed)

		if (key == 112):  # press 'P'
			pause = True
			print "VIDEO PAUSED (press any key to RESUME)"

		while pause:
			if (cv2.waitKey(-1) != -1):
				pause = False
				break 

		if (key == 115):  # press 'S'
			speed += 5
			print "video speed reduced: "+str(speed)

		if (key == 102):  # press 'F'
			if speed != 5:
				speed -= 5
				print "video speed augmented: "+str(speed)


		if (key == 98):   # press 'B'
			bw = not bw

		if (key == 114):  # press 'R'
			doRS = False
			print "Frame capture reset"

		if (key == 32):   # press SPACE
			doRS = True
			capture = frame.copy()
			print "Frame captured"

		if bw:
			frame = cv2.cvtColor(frame,cv.CV_RGB2GRAY)

			if doRS:
				BWcapture = cv2.cvtColor(capture,cv.CV_RGB2GRAY)

		cv2.imshow("ORIGINAL",frame)
		cv.MoveWindow("ORIGINAL",700,450)

		if doRS:
			if bw:
				if debugging:
					cv2.imshow("frame capture",BWcapture)
					cv.MoveWindow("frame capture",150,450)

				cv2.imshow("blur",frame - BWcapture)  #"Snippet [Raw substraction]",frame - BWcapture)

			else:
				if debugging:
					cv2.imshow("frame capture",capture)
					cv.MoveWindow("frame capture",150,450)

				cv2.imshow("Snippet [Raw substraction]",frame - capture)
			
	
		if debugging:
			cv2.imshow("FAMILY GUY Snippet [ORIGINAL]",frameOriginal)
			cv.MoveWindow("FAMILY GUY Snippet [ORIGINAL]",150,50)

		if (key == 27 or key == 113):
			print "Quit"
			break



if __name__ == '__main__':
	main()


