from __init__ import *

visualizer = CamSource(
  	Window(processors=[
  		GrayScaleProcessor(),
  		ThresholdProcessor(),
		ContoursProcessor()
	]),
	DebugWindow()
)
visualizer.show()
