from __init__ import *

visualizer = CamSource(
	Window(processors=[
		GrayScaleProcessor(),
		DFTProcessor(flags=DFTProcessor.invs),
		DFTProcessor(flags=None),
		FormatInt8()
	])
)
visualizer.show()
