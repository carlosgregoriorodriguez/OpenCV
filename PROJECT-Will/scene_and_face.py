#               PROJECT - Video Analysis
#    Detects faces in the video, draws a rectangle around them
#  Analizies the faces to see if they belong to a know character
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

# Method used for calculating the distance between histograms and threshold
method_dict = ['CORRELATION' , 'CHISQUARE' , 'INTERSECT', 'BHATTACHARYYA' ]
method = cv.CV_COMP_CHISQR
method_THRESHOLD = 3000

bins = np.arange(256).reshape(256,1)


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

def getHistogram(img):

	# First calculate histogram
	histogram = cv2.calcHist([img],[0],None,[256],[0,255]) 
	
	# Normalize obtained histogram	
	cv2.normalize(histogram,histogram,0,255,cv2.NORM_MINMAX)
		
	return histogram


def printHistogram(histogram,canvas):

	h = np.int32(np.around(histogram))
	pts = np.column_stack((bins,h))
	color = 50

	cv2.polylines(canvas,np.array([pts],np.int32),False,color,2)

	return canvas


def reduce(img):

	result = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(img)))))

	return result

# Create black image from which to compare the Raw-Substraction
black = np.zeros((368,480),dtype=np.uint8)
baseHist = getHistogram(img= black)

def compareFrames(prev_scene,actual_frame):

	newSc = False

	prev = reduce(prev_scene)
	actual = reduce(actual_frame)

	frame_dif = cv2.absdiff(prev,actual)
	histogram = getHistogram(frame_dif)
	
	if debugging:
		frame_dif = printHistogram(histogram= histogram, canvas= frame_dif)
		cv2.imshow("FRAME-DIF",frame_dif)

	distance = cv2.compareHist(histogram,baseHist,method)

	if debugging:
		print '          '+str(distance)

	if distance > method_THRESHOLD:
		newSc = True

	return newSc, distance


def getScreenPos(n):

	width = (n%6)*190 + 50

	height = None
	aux = n%18
	if aux < 6:
		height = 270
	elif aux < 12:
		height = 410
	else:
		height = 550

	return width, height


def drawString(text, (x, y), img):

	cv2.putText(img, text, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 0), 3, cv2.CV_AA)
	cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 255),1, cv2.CV_AA)


def addNewScene(scenes, new_scene, distance):

	n = len(scenes)
	print 'New scene detected'
	scenes.append(new_scene)

	drawString(method_dict[method]+"  "+distance , (20,20),new_scene)

	width,height = getScreenPos(n= n)
	cv2.imshow("Scene %d"%(n),cv2.pyrDown(new_scene))
	cv.MoveWindow("Scene %d"%(n),width,height)


def addRepScene(copies, new_scene, rep_scene, distance, drep):

	n = len(copies)
	print 'Repeated scene detected (copy of scene %d)'%(rep_scene)
	copies.append(new_scene)

	drawString(method_dict[method]+"  "+distance , (20,20),new_scene)
	drawString('with scene %d'%(rep_scene)+"  "+drep, (10,100),new_scene)

	width,height = getScreenPos(n= rep_scene)
	cv2.imshow("Scene %d - COPY%d"%(rep_scene ,n),cv2.pyrDown(new_scene))
	cv.MoveWindow("Scene %d - COPY%d"%(rep_scene ,n),width,height+20)

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

	# Create list in which new scene frames are stored
	scenes = []
	copies = []


	while True:

		frameCounter += 1
		
		#fps
		before = time.time()

		if not pause:
			succesFlag , frameOriginal = vid.read()
			frame = cv2.cvtColor(frameOriginal,cv.CV_RGB2GRAY)

		prev_scene = frame.copy()

		addNewScene(scenes= scenes, new_scene= frame, distance= "SPACE")
		cv2.imshow("Previous scene",cv2.pyrDown(frameOriginal))


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

			print "speed: "+str(speed)

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





		newScene, distance = compareFrames(prev_scene= prev_scene, actual_frame= frame)

		if newScene:
			# wait = True

			new_scene = frame.copy()

			rep_scene = 0
			drep = None
			repeated = True

			for other in scenes:
				repeated, drep = compareFrames(prev_scene= other, actual_frame= new_scene)

				if debugging:
					print str(rep_scene)+'  '+str(drep)

				if not repeated:
					break

				rep_scene += 1

			prev_scene = new_scene	

			if not repeated:
				addRepScene(copies= copies, new_scene= new_scene, rep_scene= rep_scene, distance= str(distance), drep= str(drep))

			else:
				addNewScene(scenes= scenes, new_scene= new_scene, distance= str(distance))

			cv2.imshow("Previous scene",cv2.pyrDown(frameOriginal))








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
