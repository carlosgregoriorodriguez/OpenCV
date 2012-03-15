from __init__ import *

visualizer = CamSource(
	Window(processors=[DilateProcessor()])
)
visualizer.show()
