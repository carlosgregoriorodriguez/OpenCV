from __init__ import *

#Solo funciona con GrayScaleProcessor
visualizer = CamSource(
	Window(processors=[
		BlurProcessor(),
		CannyProcessor()
	]),
	DebugWindow()
)
visualizer.show()
