from __init__ import *

visualizer = CamSource(
	Window(processors=[
		PyrDownProcessor(),
		GrayScaleProcessor(),
		DFTProcessor(flags=None),
		SobelProcessor(ddepth=0),
		DFTProcessor(flags=DFTProcessor.invs),FormatInt8()
	]),
	DebugWindow()
)
visualizer.show()
