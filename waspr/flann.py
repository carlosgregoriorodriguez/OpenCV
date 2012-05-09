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
scale = 0.2

template = SimpleCV.Image("images/wasp73.png")

while not display.isDone():
	before = time.time()
	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	img = vc.getImage().scale(scale) #.bilateralFilter() #.flipHorizontal()
	result = img.drawKeypointMatches(img,template,300.00,0.4)
	fps = 1/(time.time()-before)
	if normaldisplay:
		img.drawText('%d fps'%fps,0,0)
		img.show()
	else:
		result.show()