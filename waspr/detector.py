import SimpleCV
import colorsys
import time
from pyheat import HeatMap
import random
import cv
from PIL import Image
import pygame
from heatmap import Heatmap, Point

display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("video.mts", "video")
normaldisplay = True
scale = 0.18
hm = None
points = []

class Swarm(object):
	frame = 0
	def __init__(self):
		pass

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
					if distance[circle.x,circle.y]:
						yield color, circle
						break
class Wasp(object):
	colors = [
		(133,226,157), # Soft Green
		(62,90,149), # Deep Blue
		(110,160,220) # Soft Metalized Blue
	]

sw = Swarm()

while not display.isDone():
	before = time.time()
	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	img = vc.getImage().scale(scale) #.bilateralFilter() #.flipHorizontal()
	if not hm:
		hm = Heatmap(img.width, img.height)

	for color, circle in sw.find_wasps(img):
		radius = circle.radius()
		img.drawCircle((circle.x, circle.y), radius,SimpleCV.Color.RED,min(radius,2))
		hm.addPoint(Point(circle.x,circle.y), 10)

	fps = 1/(time.time()-before)
	if normaldisplay:
		img.drawText('%d fps'%fps,0,0)
		img.show()
	else:
		#hm.transform_color(.3)
		#image_heat = hm.get_PIL()
		image_heat = hm.transform()
		surface = pygame.image.fromstring(image_heat.tostring(), image_heat.size, image_heat.mode)
		heat = SimpleCV.Image(surface)
		heat.show()
		#mix.show()
