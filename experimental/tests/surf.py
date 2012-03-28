from __init__ import *

visualizer = CamSource(
  	Window(processors=[
  		#ThresholdProcessor(),
  		SurfProcessor(),
	]),
	DebugWindow()
)
visualizer.show()
