#               PROJECT - Video Analysis
#    Press SPACE to capture frame 
#
#    Press 'P' to pause video. To resume press any key
#    Press 'F' to make video faster
#    Press 'S' to make video go slower
#    Press 'R' to clear Histograms window
#
#    Willie - week 2 a.P. (after Project)


import cv2
import cv2.cv as cv
import time
import numpy as np
import random as rd

debugging = True   # Boolean variable for debugging

bins = np.arange(256).reshape(256,1)

color1 = [ (255,0,0),(0,255,0),(0,0,255) ]
color2 = [ (50,0,0),(0,50,0),(0,0,50) ]


usage = '''
USAGE:      SPACE - capture frame

            'P' - to pause. To resume press any key

            'F' - makes video run faster

            'S' - makes video run slower

            'R' - clears Histograms window

     QUIT: press either q or ESC
'''

def getHistogram(img):

	b,g,r = cv2.split(img)
	histogram = []
	#cv2.imshow("blue",b)
	#cv2.imshow("green",g)
	#cv2.imshow("red",r)

	for channel in [b,g,r]:

		# First calculate histogram
		hist = cv2.calcHist([img],[0],None,[256],[0,255]) 
		
		# Normalize obtained histogram	
		cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)

		histogram.append(hist)
		#print str(channel == b)

	print len(histogram)	
	return histogram


def printHistogram(img,canvas,fade):

	b,g,r = cv2.split(img)

	if fade:
		color = color2

	else:
		color = color1

	for channel,clr in zip([b,g,r],color):
		hist_item = cv2.calcHist([channel],[0],None,[256],[0,255])
		cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
	
		histogram = np.int32(np.around(hist_item))
		pts = np.column_stack((bins,histogram))
		
		cv2.polylines(canvas,np.array([pts],np.int32),False,clr,2)


	return canvas


def main():

	print usage

	pause = False
	speed = 20
	fade = True

	vid = cv2.VideoCapture("videos/FamilyGuy.mp4")

	# Create list in which captured frames are stored
	frames = []

	histResult = np.zeros((300,255,3))

	# Create window
	cv2.namedWindow("Histograms")
	cv.MoveWindow("Histograms",600,20)

	while True: 

		if not pause:
			succesFlag , frameOriginal = vid.read()
			#frame = cv2.cvtColor(frameOriginal,cv.CV_RGB2GRAY)
			frame = frameOriginal.copy()

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

		if (key == 114):  # press 'R'
			histResult = np.zeros((300,255,3))
			print "Histograms window cleared"


		if (key == 32):   # press SPACE
			print fade

			n = len(frames)
			print "Frame %d captured"%(n)
			capture = frame.copy()
			frames.append(capture)


			#hist = getHistogram(img= capture)

			histResult = printHistogram(img= capture, canvas= histResult, fade= fade)
			fade = not fade
			#print histResult

			capture = printHistogram(img= capture, canvas= capture, fade= False)

			cv2.imshow("frame %d capture"%(n),capture)
			a = None
			if (n%12 < 6):
				a = 410
			else:
				a = 550
			cv.MoveWindow("frame %d capture"%(n),(n%6)*190 + 50,a)

		#hh = getHistogram(img= frame)
		frame = printHistogram(img= frame, canvas= frame, fade= False)
		
		cv2.imshow("ORIGINAL",frame)
		cv.MoveWindow("ORIGINAL",50,20)

		if (len(frames) > 0):
			#for img in frames:

			cv2.imshow("Histograms",histResult)  
	
		if debugging:
			cv2.imshow("FAMILY GUY Snippet [ORIGINAL]",cv2.pyrDown(frameOriginal))
			cv.MoveWindow("FAMILY GUY Snippet [ORIGINAL]",800,415)

		if (key == 27 or key == 113):
			print "Quit"
			break



if __name__ == '__main__':
	main()


