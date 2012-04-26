#               PROJECT - Video Analysis
#    Press SPACE to capture frame from then on the video will be
#      the raw substraction of the fram capture form the original video
#
#    Press 'R' to reset capture frame
#    Press 'B' to toggle between b/w and color video
#
#    Willie - week 2 a.P. (after Project)


import cv2
import cv2.cv as cv
import time
import numpy as np

usage = '''
USAGE:      SPACE - capture frame. From then on the video will be the raw
                substraction of the fram capture form the original video

            'R' - reset video.

            Press 'B' to toggle between b/w and color

     QUIT: press either q or ESC
'''


def main():

	print usage

	doRS = False
	bw = False

	vid = cv2.VideoCapture("videos/FamilyGuy.mp4")

	while True: 

		succesFlag , frame = vid.read()
		#frame = frameOriginal.copy()

		key = cv2.waitKey(5)

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

		if doRS:
			if bw:
				cv2.imshow("frame capture",BWcapture)
				cv2.imshow("Snippet [Raw substraction]",frame - BWcapture)

			else:
				cv2.imshow("frame capture",capture)
				cv2.imshow("Snippet [Raw substraction]",frame - capture)
			
	
		cv2.imshow("FAMILY GUY Snippet [ORIGINAL]",frame)

		if (key == 27 or key == 113):
			print "Quit"
			break



if __name__ == '__main__':
	main()



