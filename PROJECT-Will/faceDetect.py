#               PROJECT - Video Analysis
#  Detects faces in the video and draws a rectangle around them
#
#    Willie - week 7 a.P. (after Project)

import cv2
import cv2.cv as cv
import numpy as np
import random as rd
import sys
import time

debugging = True

#Load classifier
cascade_file = "classifier/face.xml"
cascade = cv2.CascadeClassifier(cascade_file)


usage = '''
USAGE:     
		Press SPACE on first scene to start running the face detection

            'P' - to pause/resume

            'F' - makes video run faster

            'S' - makes video run slower

            'R' - sets longer spacing between face detections (increases speed)

            'W' - sets smaller spacing between face detections (decreases speed)

     QUIT: press either q or ESC
'''

def drawString(text, (x, y), img):

	cv2.putText(img, text, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 0), 3, cv2.CV_AA)
	cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 255),1, cv2.CV_AA)

def faceDetect(frame):

	minSize = (25,25)
	maxSize = (100,100)
	scaleFactor = 1.1
	minNeighbors = 3
	flags = 0

	faces = cascade.detectMultiScale(frame, scaleFactor, minNeighbors, flags, minSize, maxSize)
	return faces
	#showFaces(frame= frame, faces=faces)


def showFaces(frame, faces):

	for face_rect in faces:
		print face_rect #x_0,y_0,width,height
		cv2.rectangle(frame,(face_rect[0],face_rect[1]),(face_rect[0]+face_rect[2],face_rect[1]+face_rect[3]),(255,0,0))            

	return frame



def main():

	print usage

	pause = False
	speed = 20
	frameWait = 15
	frameCounter = 0
	faces = None


	# Load video
	filename = "videos/Joey.mp4";
	if (len(sys.argv)>1):
		filename = sys.argv[1];
	vid = cv2.VideoCapture(filename) # MontyPython.mp4 FamilyGuy.mp4  FamGuy2.mp4  FamGuy3.mp4  FamGuy4.mp4


	while True:

		frameCounter += 1
		
		#fps
		before = time.time()

		if not pause:
			succesFlag , frameOriginal = vid.read()
			frame = cv2.cvtColor(frameOriginal,cv.CV_RGB2GRAY)

		while not succesFlag:
			print "Lost frame... trying again"
			succesFlag,frameOriginal = vid.read()
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
			if speed > 5:
				speed -= 5
				
			elif speed > 1:
				speed -= 1

		if (key == 114):  # press 'R'
			frameWait += 5
			print "face-detection each "+str(frameWait)+" frames."

		if (key == 119):  # press 'W'
			if frameWait > 5:
				frameWait -= 5
				
			elif frameWait > 1:
				frameWait -= 1
			print "face-detection each "+str(frameWait)+" frames."

		if frameCounter > frameWait:
			faces = faceDetect(frame)
			frameCounter = 0

		if faces != None:
			frame = showFaces(frame= frame, faces= faces)

		#fps
		fps = 1/(time.time()-before)

		# Show original video
		drawString("fps : "+str(fps), (20 ,20 ), frameOriginal)
		cv2.imshow("ORIGINAL",cv2.pyrDown(frameOriginal))

		# Show detected faces
		cv2.imshow("FACES",frame)
		cv.MoveWindow("FACES",100,100)


		if (key == 27 or key == 113): #QUIT
			print "Quit"
			break




if __name__ == '__main__':
	main()
