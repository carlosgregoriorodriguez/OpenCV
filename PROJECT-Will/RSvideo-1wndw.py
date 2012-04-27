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

imgWidth = 480
imgHeight = 368 


def main():

	print usage

	doRS = False
	bw = False

	vid = cv2.VideoCapture("videos/FamilyGuy.mp4")

	while True: 

		succesFlag , frame = vid.read()
		#frame = cv2.resize(src=frameOriginal, dsize=(imgWidth,imgHeight))
		BWframe = cv2.cvtColor(frame,cv.CV_RGB2GRAY)

		result = np.zeros((imgHeight,imgWidth*3,3),np.uint8)
		resultBW = np.zeros((imgHeight,imgWidth*3),np.uint8)

		key = cv2.waitKey(5)

		if (key == 98):   # press 'B'
			bw = not bw

		if (key == 114):  # press 'R'
			doRS = False
			print "Frame capture reset"

		if (key == 32):   # press SPACE
			doRS = True
			capture = frame.copy()
			BWcapture = cv2.cvtColor(capture,cv.CV_RGB2GRAY)
			print "Frame captured"

		
		if doRS:
			if bw:
				
				for x in range(imgHeight):
					for y in range(imgWidth):
						#cv2.imshow("frame capture",BWcapture)
						resultBW[x,2*imgWidth+y] = BWcapture[x,y]

						#cv2.imshow("Snippet [Raw substraction]",frame - BWcapture)
						resultBW[x,imgWidth+y] = BWframe[x,y] - BWcapture[x,y]


			else:
				
				for c in range(3):
					
					for x in range(imgHeight):
						for y in range(imgWidth):
							#cv2.imshow("frame capture",capture)
							result[x,2*imgWidth+y,c] = capture[x,y,c]

							#cv2.imshow("Snippet [Raw substraction]",frame - capture)			
							result[x,imgWidth+y,c] = frame[x,y,c] - capture[x,y,c]

				
		
		for x in range(imgHeight):
			for y in range(imgWidth):
				#cv2.imshow("FAMILY GUY Snippet [ORIGINAL]",frame)
				resultBW[x,y] = BWframe[x,y]
				result[x,y] = frame[x,y]

		if bw:
			cv2.imshow("Family Guy color Snippet",result)

		else:
			cv2.imshow("Family Guy color Snippet",resultBW)


		if (key == 27 or key == 113):
			print "Quit"
			break



if __name__ == '__main__':
	main()



