from __init__ import *

visualizer = CamSource(
	Window(processors=[ErodeProcessor()])
)
visualizer.show()
