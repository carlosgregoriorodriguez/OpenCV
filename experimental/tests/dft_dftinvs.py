from __init__ import *

visualizer = CamSource(
	Window(processors=[
		GrayScaleProcessor(),
		DFTProcessor(flags=None),
		DFTProcessor(flags=DFTProcessor.invs),
		FormatInt8()
	]),
        DebugWindow()
)
visualizer.show()
