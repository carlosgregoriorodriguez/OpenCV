import SimpleCV
import colorsys
import time

display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("video.mts", "video")
normaldisplay = True
rgb_color_indicators = [
	(133,226,157), # Soft Green
	(62,90,149), # Deep Blue
	(93,172,242), # Soft Blue
]
# hsv_color_indicators = [colorsys.rgb_to_hls(*c) for c in rgb_color_indicators]
scale = 0.2
while not display.isDone():
	before = time.time()
	candidates = []

	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	img = vc.getImage().scale(scale) #.bilateralFilter() #.flipHorizontal()
	for color in rgb_color_indicators:
		dist = img.colorDistance(color).invert().dilate() #hueDistance
		segmented = dist.stretch(215,255)
		blobs = segmented.findBlobs() or []
		candidates += blobs
	if candidates:
		#circles = blobs
		#circles = candidates.filter([b.isCircle(.3) for b in candidates])
		for circle in candidates:
			radius = circle.radius()
			if 3*scale<radius<36*scale: img.drawCircle((circle.x, circle.y), radius,SimpleCV.Color.RED,min(radius,3))

	fps = 1/(time.time()-before)

	if normaldisplay:
		img.drawText('%d fps'%fps,0,0)
		img.show()
	else:
		segmented.show()
