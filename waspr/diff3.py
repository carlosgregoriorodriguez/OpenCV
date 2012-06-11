import SimpleCV
import colorsys
import time

display = SimpleCV.Display()
vc = SimpleCV.VirtualCamera("video.mts", "video")
normaldisplay = True
clean = SimpleCV.Image('images/clean.png')

scale = 0.2
blobs = []
kernel = [[1,1,-1],[2,1,-2],[1,-1,1]]
kernel = [[1,2],[-1,2]]
cleans = clean.convolve(kernel).scale(scale)
while not display.isDone():
	if display.mouseRight:
		normaldisplay = not(normaldisplay)
	before = time.time()
	vcimg = vc.getImage().crop(0,0,1920,1080)
	img = vcimg.scale(scale).convolve(kernel) #.bilateralFilter() #.flipHorizontal()
	diff = cleans-img
	#diff = diff.binarize(-1)
	diff = diff.binarize(-1).grayscale().dilate(1).erode(2)
	blobs = (diff.invert()).findBlobs()
	
	if blobs:
		for blob in blobs:
			img.drawCircle((blob.x, blob.y), 10,SimpleCV.Color.RED,3)

	fps = 1/(time.time()-before)
	if normaldisplay:
		diff.drawText('%d fps'%fps,0,0)
		diff.show()
	else:
		img.show()
