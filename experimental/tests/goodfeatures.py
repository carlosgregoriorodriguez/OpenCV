from __init__ import *

visualizer = CamSource(
	Window(processors=[GoodFeaturesProcessor()])
)
visualizer.show()
