import SimpleCV
import colorsys
import time
from pyheat import HeatMap
import random
import cv
from PIL import Image
import pygame

display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("video.mts", "video")
normaldisplay = False
rgb_color_indicators = [
	(133,226,157), # Soft Green
	(62,90,149), # Deep Blue
	# (93,172,242), # Soft Blue
	# (115,156,212), # Soft Metalized Blue
	(110,160,220), # Soft Metalized Blue
]
# hsv_color_indicators = [colorsys.rgb_to_hls(*c) for c in rgb_color_indicators]
scale = 0.18
blobs = []
hm = None
points = []
while not display.isDone():
	before = time.time()
	candidates = []
	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	img = vc.getImage().scale(scale) #.bilateralFilter() #.flipHorizontal()
	if not hm:
		hm = HeatMap(0, img.width, 0, img.height)
		hm.invert_y = True
	distances = {}
	for color in rgb_color_indicators:
		distances[color] = img.colorDistance(color).invert().binarize(225,255).erode(2).dilate(1).invert() #hueDistance
		# if a: dist = dist | a #dist.stretch(215,255)
		# a = dist
	mix = reduce(lambda x,y:x | y, distances.values())
	blobs = mix.findBlobs() or []
	candidates += blobs or []
	if candidates:
		#circles = blobs
		#circles = candidates.filter([b.isCircle(.3) for b in candidates])
		for circle in candidates:
			radius = circle.radius()+2
			if 6*scale+2<radius<36*scale:
				img.drawCircle((circle.x, circle.y), radius,SimpleCV.Color.RED,min(radius,2))

		points = [(circle.x, circle.y) for circle in candidates]
		hm.add_points(points, 12)

	fps = 1/(time.time()-before)
	if normaldisplay:
		img.drawText('%d fps'%fps,0,0)
		img.show()
	else:
		hm.transform_color(.3)
		image_heat = hm.get_PIL()
		surface = pygame.image.fromstring(image_heat.tostring(), image_heat.size, image_heat.mode)
		heat = SimpleCV.Image(surface)
		heat.show()
		#mix.show()
