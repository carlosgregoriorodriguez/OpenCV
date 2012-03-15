from __init__ import *

visualizer = CamSource(
	Window(processors=[MeanShiftFilteringProcessor()])
)
visualizer.show()
