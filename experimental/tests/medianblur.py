from __init__ import *

visualizer = CamSource(
	Window(processors=[MedianBlurProcessor()])
)
visualizer.show()
