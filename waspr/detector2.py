import SimpleCV
import colorsys
import time
from pyheat import HeatMap
import random
import cv
from PIL import Image
import pygame
from heatmap import Heatmap, Point
import numpy as np
from scipy import spatial
import math
from multiprocessing import Process
from SimpleCV.Display import pg
display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("video.mts", "video")
normaldisplay = True
scale = 0.5
hm = None

import math

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


class Swarm(object):
	def __init__(self,processor = lambda x:x):
		self.frame = 0
		self.processor = processor
		self.wasps = []

	def _get_clean(self):
		return self._clean

	def _set_clean(self,clean):
		self._clean = self.processor(clean)

	clean = property(_get_clean,_set_clean)

	def find_wasps(self,img):
		# img = self.processor(img)
		distances = {}
		for color in Wasp.colors:
			distances[color] = img.colorDistance(color).invert().binarize(225,255).erode(2).dilate(1).invert() #hueDistance

		mix = reduce(lambda x,y:x | y, distances.values())
		candidates = mix.findBlobs() or []
		
		processed_img = self.processor(img)

		diff = (self.clean-processed_img).binarize(-1).grayscale().invert().erode(1).dilate(2) | mix.dilate(2)
		diff_blobs = diff.findBlobs(minsize=40)

		self.diff_blobs = diff_blobs
		# if diff_blobs:
		# 	diff_blobs = diff_blobs.filter(diff_blobs.area() > 1)
		# if diff_blobs: diff_blobs.show(autocolor=True)
		for circle in candidates:
			center = (circle.x,circle.y)
			#center = circle.centroid()
			next_blob = diff_blobs.sortDistance(point=center)[0]
			blob_center = next_blob.centroid() #(next_blob.x,next_blob.y)
			try:
				vector = (blob_center[0]-center[0],blob_center[1]-center[1])
				a = angle(vector,(1,0))
			except:
				a = None
			# diff.drawLine(center,blob_center,SimpleCV.Color.YELLOW,2)
			radius = circle.radius()+2
			if 6*scale+2<radius<36*scale:
				for color,distance in distances.items():
					if distance[circle.x,circle.y][0]:
						yield color, circle, a
						break
		# diff.show()

	def relation_wasps(self,ccs):
		next_positions, prev_positions = {}, {}
		for color,circle,_ in ccs:
			if color not in next_positions: next_positions[color] = []
			next_positions[color].append((circle.x,circle.y))

		if self.wasps:
			for wasp in self.wasps:
				if wasp.color not in prev_positions: prev_positions[wasp.color] = []
				prev_positions[wasp.color].append(wasp.last_position)


			for color, positions in next_positions.items():
				tree = spatial.KDTree(positions)
				print tree.data

		else:
			pass

	def advance(self):
		self.frame += 1

class Wasp(object):
	COLOR_SOFTGREEN = (133,226,157)
	COLOR_DEEPBLUE = (62,90,149)
	COLOR_SOFTBLUE = (110,160,220)
	colors = [
		COLOR_SOFTGREEN,
		COLOR_DEEPBLUE,
		COLOR_SOFTBLUE
	]

	def __init__(self,frame=0):
		self.last_frame = frame
		self.positions = []
		self._color = None

	@property
	def last_position(self):
		return self.positions[-1] if self.positions else None

	def update_position(self,position,frame):
		steps = frame-self.last_frame
		if steps<1: return
		elif steps==1: self.positions.append(position)
		else:
			last_position = self.last_position
			self.positions += zip(
				np.linspace(last_position[0],position[0],steps),
				np.linspace(last_position[1],position[1],steps))[1:]

clean = SimpleCV.Image('images/clean.png')
scale= 1
sw = Swarm(lambda x:x.convolve([[1,2],[-1,2]]))
sw.clean = clean.scale(scale)

wasplayer = SimpleCV.DrawingLayer(sw.clean.size())
wasplayer.setDefaultAlpha(100)
painting = False
paused = False
while not display.isDone():
	before = time.time()
	display.checkEvents()
	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	if display.mouseLeft:
		painting = not painting
	key =  pg.key.get_pressed()
	if key[ord('p')]:
		paused = not paused
		if paused:
			img.addDrawingLayer(wasplayer)

	#print dir(display)
	#print display.leftButtonDown, display.leftButtonDownPosition()
	if painting and paused:
		wasplayer.circle((display.mouseRawX, display.mouseRawY), 30, filled=True, color=SimpleCV.Color.GREEN)
	
	if not paused:
		img = vc.getImage().crop(0,0,clean.width,clean.height).scale(scale) #.bilateralFilter() #.flipHorizontal()

	if False:
		wasps = list(sw.find_wasps(img))
		sw.relation_wasps(wasps)
		#img = img.scale(.2)

		procs = []
		for color, circle, a in wasps:
			center = (circle.x, circle.y)
			if a:
				external_point = (int(center[0]+ math.cos(a)*100*scale), int(center[1]+scale*100*math.sin(a)))
				img.drawLine(center,external_point,SimpleCV.Color.YELLOW,2)
			radius = circle.radius()
			img.drawCircle(center, radius,color,min(radius,scale*10))
		sw.advance()
	# img.show()
	fps = 1/(time.time()-before)
	if normaldisplay:
		if not paused:
			img.drawText('%d fps'%fps,0,0)
			img.show()
		else:
			mask = SimpleCV.Image(img.size())
			mask.addDrawingLayer(wasplayer)
			mask = mask.applyLayers().binarize().invert().dilate(30)
			a = img.applyBinaryMask(mask)
			circles = a.findCircle(thresh=200)
			if circles:
				print '*******',circles
				a = circles[0]
			#img = img.findCircle()[0]
			a.show()
	else:
		# sw.diff_blobs.drawText('%d fps'%fps,0,0)
		sw.diff_blobs.show(autocolor=True)
		#hm.transform_color(.3)
		#image_heat = hm.get_PIL()
		# image_heat = hm.transform()
		# surface = pygame.image.fromstring(image_heat.tostring(), image_heat.size, image_heat.mode)
		# heat = SimpleCV.Image(surface)
		# heat.show()
		#mix.show()
