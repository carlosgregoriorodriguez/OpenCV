import SimpleCV
import time
display = SimpleCV.Display()
img = SimpleCV.Image("snap.png")
color = (133,255,146)
paso1 = img.colorDistance(color).invert().dilate()
paso2 = paso1.dilate(2).stretch(220,255).invert()
while not display.isDone():
	paso2.show()