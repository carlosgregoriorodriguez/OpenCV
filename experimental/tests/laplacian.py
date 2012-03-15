from __init__ import *

visualizer = CamSource(
	Window(processors=[LaplacianProcessor()])
)
visualizer.show()
