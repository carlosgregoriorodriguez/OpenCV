#               PROJECT - Video Analysis
#    Program for calculating difference between frame captures.
#
#    Willie - week 2 a.P. (after Project)


import cv2
import cv2.cv as cv
import time
import numpy as np
import sys

usage = '''
USAGE:      python frameDif.py [frame 1] [frame 2]

     QUIT: press either q or ESC
'''

def main():

	print usage

	img1 = cv2.imread("frames/frame2.jpg",0)   #img1 = cv2.imread(sys.argv[1])
	img2 = cv2.imread("frames/frame4.jpg",0)   #img2 = cv2.imread(sys.argv[2])

	cv2.imshow("FRAME 1",img1)
	cv2.imshow("FRAME 2",img2)

	while True:

		cv2.imshow("frame DIFFERENCE",img1 - img2)

		key = cv2.waitKey(5)

		if (key == 27 or key == 113):
			print "Quit"
			break

if __name__ == '__main__':
	main()
