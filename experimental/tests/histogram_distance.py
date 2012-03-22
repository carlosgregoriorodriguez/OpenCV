from __init__ import *

visualizer = CamSource(
  Window(processors=[HistogramDistanceProcessor()]),
  Window(processors=[HistogramProcessor()])
)
visualizer.show()
