from __init__ import *

visualizer = CamSource(
	Window(processors=[BoxFilterProcessor()])
)
visualizer.show()
