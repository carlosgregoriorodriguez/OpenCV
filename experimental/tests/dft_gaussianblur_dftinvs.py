from __init__ import *

visualizer = CamSource(
	Window(processors=[
		PyrDownProcessor(),
		GrayScaleProcessor(),
		DFTProcessor(flags=None),
		GaussianBlurProcessor(),
		DFTProcessor(flags=DFTProcessor.invs),FormatInt8()
	]),
	DebugWindow()
)
visualizer.show()
