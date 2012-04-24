import SimpleCV

display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("00219.mts", "video")
normaldisplay = True

colors = [SimpleCV.Color.RED, SimpleCV.Color.GREEN, SimpleCV.Color.MAROON]
while not display.isDone():
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

	if normaldisplay:
		img.show()
	else:
		segmented.show()
