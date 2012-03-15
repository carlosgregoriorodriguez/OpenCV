from __init__ import *

visualizer = CamSource(
	Window(processors=[PyrDownProcessor()])
)
visualizer.show()
