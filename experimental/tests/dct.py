from __init__ import *

visualizer = CamSource(
	Window(processors=[
		GrayScaleProcessor(),
		DCTProcessor(flags=None),
		FormatInt8()
	])
)
visualizer.show()
