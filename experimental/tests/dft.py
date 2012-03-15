from __init__ import *

visualizer = CamSource(
	Window(processors=[
		GrayScaleProcessor(),
		DFTProcessor(flags=None),
		FormatInt8()
	])
)
visualizer.show()
