from __init__ import *

visualizer = CamSource(
  Window(processors=[AdaptiveThresholdProcessor()])
)
visualizer.show()
