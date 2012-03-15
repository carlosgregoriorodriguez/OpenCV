from __init__ import *

visualizer = CamSource(
	Window(processors=[
		PyrDownProcessor(),
		GrayScaleProcessor(),
		DCTProcessor(flags=None),
		GaussianBlurProcessor(),
		DCTProcessor(flags=DCTProcessor.inverse),
		FormatInt8()
	]),
	DebugWindow()
)
visualizer.show()
