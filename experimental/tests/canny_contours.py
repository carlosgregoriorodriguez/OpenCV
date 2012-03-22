from __init__ import *

#Solo funciona con GrayScaleProcessor
visualizer = CamSource(
	Window(processors=[
		CannyProcessor(),
		ContoursProcessor()
	]),
	DebugWindow()
)
visualizer.show()
