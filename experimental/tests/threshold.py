from __init__ import *

visualizer = CamSource(
  Window(processors=[ThresholdProcessor()])
)
visualizer.show()
