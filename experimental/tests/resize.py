from __init__ import *

visualizer = CamSource(
	Window(processors=[ResizeComplexTrackbarProcessor()])
)
visualizer.show()
