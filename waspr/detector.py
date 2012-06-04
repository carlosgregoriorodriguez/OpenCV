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

display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("video.mts", "video")
normaldisplay = True
scale = 0.3
hm = None

def get_direction(img,center,radius):
	num = 300
	theta = np.linspace(0,2*math.pi,num)
	is_black= False
	black, white = 0, 0
	can_white = False
	black_white = [] #(is_black,theta)
	candidates = []
	for t in theta:
		x = center[0]+radius*math.cos(t)
		y = center[1]+radius*math.sin(t)
		c = img.getPixel(int(x),int(y))[0]
		last_black = t if black>=5 else False
		last_white = t if white>=5 and white<=20 else False
		if c==0:
			if last_white: black_white.append((False,last_white,white))
			black +=1
			white = 0
			#processed.dl().circle((x,y),2,SimpleCV.Color.GREEN)
		else:
			if last_black: black_white.append((True,last_black,black))
			black = 0
			white +=1

	if len(black_white)>=3:
		for i in range(len(black_white)-2):
			if black_white[i][0]==black_white[i+2][0]==True and not black_white[i+1][0]:
				old_t = black_white[i+1][1]
				adjusted_t = old_t-(math.pi/num)*black_white[i+1][2]-0.02
				candidates.append(adjusted_t)

	max_r = radius*2.3
	for c in candidates:
		#processed.drawLine(center,(center[0]+ math.cos(c)*r, center[1]+r*math.sin(c)),SimpleCV.Color.BLUE)
		external_point = (int(center[0]+ math.cos(c)*max_r), int(center[1]+max_r*math.sin(c)))
		if img.getPixel(*external_point)[0]==0 or len(candidates)==1:
			return c
			#processed.drawLine(center,external_point,SimpleCV.Color.YELLOW,2)
	return None


class Swarm(object):
	def __init__(self):
		self.frame = 0
		self.wasps = []

	def find_wasps(self,img):
		distances = {}
		for color in Wasp.colors:
			distances[color] = img.colorDistance(color).invert().binarize(225,255).erode(2).dilate(1).invert() #hueDistance

		mix = reduce(lambda x,y:x | y, distances.values())
		candidates = mix.findBlobs() or []
		for circle in candidates:
			radius = circle.radius()+2
			if 6*scale+2<radius<36*scale:
				for color,distance in distances.items():
					if distance[circle.x,circle.y][0]:
						yield color, circle
						break
	def relation_wasps(self,ccs):
		next_positions, prev_positions = {}, {}
		for color,circle in ccs:
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

sw = Swarm()

while not display.isDone():
	before = time.time()
	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	img = vc.getImage().scale(scale) #.bilateralFilter() #.flipHorizontal()
	directionimg = img.convolve([[-1,4],[-1,1]]).stretch(70,220)

	if not hm:
		hm = Heatmap(img.width, img.height)

	wasps = list(sw.find_wasps(img))
	sw.relation_wasps(wasps)

	for color, circle in wasps:
		center = (circle.x, circle.y)
		theta = get_direction(directionimg,center,50*scale)
		if theta:
			external_point = (int(center[0]+ math.cos(theta)*100*scale), int(center[1]+scale*100*math.sin(theta)))
			directionimg.drawLine(center,external_point,SimpleCV.Color.YELLOW,2)
		radius = circle.radius()
		img.drawCircle(center, radius,color,min(radius,2))
		hm.addPoint(Point(circle.x,circle.y), 10)

	sw.advance()

	fps = 1/(time.time()-before)
	if normaldisplay:
		img.drawText('%d fps'%fps,0,0)
		img.show()
	else:
		directionimg.drawText('%d fps'%fps,0,0)
		directionimg.show()
		#hm.transform_color(.3)
		#image_heat = hm.get_PIL()
		# image_heat = hm.transform()
		# surface = pygame.image.fromstring(image_heat.tostring(), image_heat.size, image_heat.mode)
		# heat = SimpleCV.Image(surface)
		# heat.show()
		#mix.show()
