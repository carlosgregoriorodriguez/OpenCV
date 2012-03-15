from __init__ import *

#Solo funciona con GrayScaleProcessor
visualizer = CamSource(
	Window(processors=[
		GrayScaleProcessor(),
		CannyProcessor()
	]),
	DebugWindow()
)
visualizer.show()
