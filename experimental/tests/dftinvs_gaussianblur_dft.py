from __init__ import *

visualizer = CamSource(
	Window(processors=[
		PyrDownProcessor(),
		GrayScaleProcessor(),
		DFTProcessor(flags=DFTProcessor.invs),
		GaussianBlurProcessor(),
		DFTProcessor(flags=None),
		FormatInt8()
	])
)
visualizer.show()
