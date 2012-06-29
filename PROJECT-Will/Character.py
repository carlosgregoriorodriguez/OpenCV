#               PROJECT - Video Analysis
#      Data structure in which all the information about 
#              a character is gathered
#   
#    Willie - week 8 a.P. (after Project)

import cv2
import cv2.cv as cv
import numpy as np

from detect_compare import getHistogram, reduce, printHistogram, compareFrames


def compareF(a,b):
	return a == b

class Character:

	def __init__(self,nm):

		self.faces = []	#List in which all the different faces of the character are stored
		self.name = nm


	def add(self, new_data):

		if len(self.faces) > 0:
			y = True

			for face in self.faces:
				y = compareF(face,new_data)
				if y:
					break
			if not y:
				self.faces.append(new_data)

		else:
			self.faces.append(new_data)

		print self

	def merge(self, other_character):

		for d in other_character.faces:
			self.add(d)

	def __str__(self):

		return self.name + str(self.faces)


	

