from __init__ import *

visualizer = CamSource(
  Window(processors=[HistogramProcessor()])
)
visualizer.show()
