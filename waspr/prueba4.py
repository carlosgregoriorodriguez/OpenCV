import SimpleCV
import colorsys
import time

display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("video.mts", "video")
normaldisplay = True
rgb_color_indicators = [
	(133,226,157), # Soft Green
	(62,90,149), # Deep Blue
	# (93,172,242), # Soft Blue
	# (115,156,212), # Soft Metalized Blue
	(110,160,220), # Soft Metalized Blue
]
# hsv_color_indicators = [colorsys.rgb_to_hls(*c) for c in rgb_color_indicators]
scale = 0.2
blobs = []
while not display.isDone():
	before = time.time()
	candidates = []
	a = None
	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	img = vc.getImage().scale(scale) #.bilateralFilter() #.flipHorizontal()
	for color in rgb_color_indicators:
		dist = img.colorDistance(color).invert().binarize(215,255).erode(1).invert() #hueDistance
		if a: dist = dist | a #dist.stretch(215,255)
		a = dist
	blobs = a.findBlobs() or []
	candidates += blobs or []
	if candidates:
		#circles = blobs
		#circles = candidates.filter([b.isCircle(.3) for b in candidates])
		for circle in candidates:
			radius = circle.radius()+2
			if 6*scale+2<radius<36*scale: img.drawCircle((circle.x, circle.y), radius,SimpleCV.Color.RED,min(radius,2))

	fps = 1/(time.time()-before)
	if normaldisplay:
		img.drawText('%d fps'%fps,0,0)
		img.show()
	else:
		a.show()
