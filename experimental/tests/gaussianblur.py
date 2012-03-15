from __init__ import *

visualizer = CamSource(
	Window(processors=[GaussianBlurProcessor()])
)
visualizer.show()
