import SimpleCV
import time
display = SimpleCV.Display()
normaldisplay = False
img = SimpleCV.Image('images/wasp1.png')
d = (16,13,14)
#cd = img.colorDistance(c)
#processed = cd.morphGradient()
#processed = cd.binarize(-1,maxv=30)
c = img.getPalette()
#a,b,c = c[0],c[1],c[6]
#print a,b,c
#a,b,c=[15, 11, 13], [51, 41, 41], [106,  94,  96]
#[126 115 121] [33 24 25] [47 36 34]
processed = img.convolve()
#processed = cd.stretch(0,25)
while not display.isDone():
	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	if normaldisplay:
		img.show()
	else:
		processed.show()
# 
# 	before = time.time()
# 	candidates = []

# 	if display.mouseRight:
# 		normaldisplay = not(normaldisplay)

# 	img = vc.getImage().scale(.3) #.flipHorizontal()
# 	for color in colors:
# 		dist = img.colorDistance(color).dilate(2)
# 		segmented = dist.stretch(180,255)
# 		blobs = segmented.findBlobs()
# 		candidates += blobs

# 	if candidates:
# 		#circles = blobs
# 		#circles = candidates.filter([b.isCircle(.8) for b in candidates])
# 		for circle in candidates:
# 			radius = circle.radius()
# 			if radius<=10:
# 				img.drawCircle((circle.x, circle.y), radius,SimpleCV.Color.RED,min(radius,3))
# 	fps = 1/(time.time()-before)

# 	if normaldisplay:
# 		img.drawText('%d fps'%fps,0,0)
# 		img.show()
# 	else:
# 		segmented.show()
