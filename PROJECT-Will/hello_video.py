#               PROJECT - Video Analysis
# BASIC example for reading a video file and showing the images.
#
#    Willie - week 1 a.P. (after Project)


import cv2
import cv2.cv as cv
import time
import numpy as np

usage = '''
USAGE:      SPACE - capture frames. (press f to toggle between b/w and color captures)
            c - color video     or      b - b/w video
            UP - apply pyrUp       DOWN - apply pyrDown

     QUIT: press either q or ESC
'''

MAXframes = 5      #Maximum number of frames allowed to store

START = cv2.getTickCount()


def clock():
    return (cv2.getTickCount() - START)/ cv2.getTickFrequency()

def captureFrame(frame,bwFR):
	time = clock()
	frameCopy = frame.copy()
	print("Frame captured")

	if bwFR:
		frameCopy = cv2.cvtColor(frameCopy,cv.CV_RGB2GRAY)

	cv2.imshow("CAPTURE %d" %(time) , frameCopy)


def main():

	print usage

	counter = 0  #FrameCapture counter, the program will quit when the counter reaches MAXframes
	bwFR = False
	bwVid = False
	pUp = False
	pDown = False

	vid = cv2.VideoCapture("videos/FamilyGuy.mp4")

	while True: 

		succesFlag , frameOriginal = vid.read()
		frame = frameOriginal.copy()

		key = cv2.waitKey(5)

		if (key == 63232 or pUp):  # UP --> Apply pyrUp
			pUp = True
			frame = cv2.pyrUp(frame)

		if (key == 63233 or pDown): # DOWN --> Apply pyrDown
			pDown = True
			frame = cv2.pyrDown(frame)

		if (key == 13): # ENTER --> End pyr's
			pDown = False
			pUp = False


		if bwVid:
			frame = cv2.cvtColor(frame,cv.CV_RGB2GRAY)

		cv2.imshow("COOKIN SOUL - Aqui te pillo aqui temazo",frame)


		if (key == 98):  # b --> Black and White VIDEO
			bwVid = True 

		if (key == 99):  # c --> Color VIDEO
			bwVid = False

		if (key == 102): # f --> Toggle between BnW / Color frame captures
			bwFR = not bwFR
			print("Black and White capture frames changed to: %r" % (bwFR) )

		if (key == 32):  #SPACE  --> Capture Frame
			captureFrame(frame = frameOriginal, bwFR = bwFR)
			counter += 1
			if (counter < MAXframes):
				print("Memory for %d more" %(MAXframes - counter))

			else: 
				print("MEMORY FULL")



		if (key == 27 or key == 113 or counter == MAXframes):  #press ESC or q to QUIT
			print("Quitting...")
			break


if __name__ == '__main__':
	main()

