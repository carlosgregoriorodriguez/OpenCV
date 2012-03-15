from __init__ import *

visualizer = CamSource(
	Window(processors=[SobelProcessor()])
)
visualizer.show()
