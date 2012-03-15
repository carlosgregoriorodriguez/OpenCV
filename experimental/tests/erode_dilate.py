from __init__ import *

visualizer = CamSource(
	Window(processors=[ErodeProcessor(),DilateProcessor()])
)
visualizer.show()
