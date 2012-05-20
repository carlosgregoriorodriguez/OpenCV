#               PROJECT - Video Analysis
#  Processes video and shows a frame capture for each new scene detected
#
#    Willie - week 4 a.P. (after Project)


import cv2
import cv2.cv as cv
import time
import numpy as np
import random as rd

debugging = False                          # Boolean variable for debugging

bins = np.arange(256).reshape(256,1)

usage = '''
USAGE:     
		Press SPACE on first scene to start running the scene detection

            'P' - to pause/resume

            'F' - makes video run faster

            'S' - makes video run slower

     QUIT: press either q or ESC
'''


# Method used for calculating the distance between histograms and threshold
method_dict = ['CORRELATION' , 'CHISQUARE' , 'INTERSECT', 'BHATTACHARYYA' ]
method = cv.CV_COMP_CHISQR
method_THRESHOLD = 3000


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

	cv2.putText(img, text, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 0), thickness = 2, linetype=cv2.CV_AA)
	cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 255, 255), linetype=cv2.CV_AA)


def addNewScene(scenes, new_scene, distance):

	n = len(scenes)
	print 'New scene detected'
	scenes.append(new_scene)

	drawString(method_dict[method]+"  "+distance , (20,20),new_scene)

	width,height = getScreenPos(n= n)
	cv2.imshow("Scene %d"%(n),cv2.pyrDown(new_scene))
	cv.MoveWindow("Scene %d"%(n),width,height)



def main():

	print usage

	started = False
	pause = False
	speed = 30
	wait = False
	wait_counter = 0
	wait_THRESHOLD = 80   # WITH   wait_THRESHOLD=100 speed=30  --> aprox. 3.8 secs

	#Create previous scene frame
	#prev_scene = black.copy()
	cv2.namedWindow("Previous scene")
	cv.MoveWindow("Previous scene",775,50)

	# Load video
	vid = cv2.VideoCapture("videos/FamilyGuy.mp4") # MontyPython.mp4 FamilyGuy.mp4  FamGuy2.mp4  FamGuy3.mp4  FamGuy4.mp4

	# Create list in which new scene frames are stored
	scenes = []

	# Create window
	cv2.namedWindow("ORIGINAL")
	cv.MoveWindow("ORIGINAL",200,50)


	while True: 

		if not pause:
			succesFlag , frameOriginal = vid.read()
			frame = cv2.cvtColor(frameOriginal,cv.CV_RGB2GRAY)

			# Show original video
			cv2.imshow("ORIGINAL",cv2.pyrDown(frameOriginal))


		key = cv2.waitKey(speed)

		if (key == 32):  # press SPACE
			started = True
			prev_scene = frame.copy()

			addNewScene(scenes= scenes, new_scene= frame, distance= "SPACE")
			cv2.imshow("Previous scene",cv2.pyrDown(frameOriginal))


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


		# Implements wait time between searching for another scene
		if wait:
			if wait_counter < wait_THRESHOLD:
				wait_counter += 1
			else:
				wait_counter = 0
				wait = False

		elif started:
			#print 'Trying to catch new scene'
			
			newScene, distance = compareFrames(prev_scene= prev_scene, actual_frame= frame)

			if newScene:
				# wait = True

				new_scene = frame.copy()

				prev_scene = new_scene				
				addNewScene(scenes= scenes, new_scene= new_scene, distance= str(distance))
				cv2.imshow("Previous scene",cv2.pyrDown(frameOriginal))

		prev_scene = frame.copy()


		if (key == 27 or key == 113):
			print "Quit"
			break



if __name__ == '__main__':
	main()

