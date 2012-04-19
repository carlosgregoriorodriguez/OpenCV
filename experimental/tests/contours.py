from __init__ import *

visualizer = CamSource(
	Window(processors=[
		GrayScaleProcessor(),
		ContoursProcessor(),
	])
)
visualizer.show()
