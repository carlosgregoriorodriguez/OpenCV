from __init__ import *

visualizer = CamSource(
	Window(processors=[BlurProcessor()])
)
visualizer.show()
