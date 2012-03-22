from __init__ import *

visualizer = CamSource(
  	Window(processors=[
  		AdaptiveThresholdProcessor(),
		ContoursProcessor()
	]),
	DebugWindow()
)
visualizer.show()
