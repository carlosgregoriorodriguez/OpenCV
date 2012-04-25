import SimpleCV
import time
display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("video.mts", "video")
normaldisplay = True

colors = [SimpleCV.Color.RED, SimpleCV.Color.GREEN, SimpleCV.Color.MAROON]
while not display.isDone():
	before = time.time()
	candidates = []

	if display.mouseRight:
		normaldisplay = not(normaldisplay)

	img = vc.getImage().scale(.3) #.flipHorizontal()
	for color in colors:
		dist = img.colorDistance(color).dilate(2)
		segmented = dist.stretch(180,255)
		blobs = segmented.findBlobs()
		candidates += blobs

	if candidates:
		#circles = blobs
		#circles = candidates.filter([b.isCircle(.8) for b in candidates])
		for circle in candidates:
			radius = circle.radius()
			if radius<=10:
				img.drawCircle((circle.x, circle.y), radius,SimpleCV.Color.RED,min(radius,3))
	fps = 1/(time.time()-before)

	if normaldisplay:
		img.show()
	else:
		segmented.show()
