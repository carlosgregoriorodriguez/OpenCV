from __init__ import *

visualizer = CamSource(
	Window(processors=[FloodFillProcessor()])
)
visualizer.show()
