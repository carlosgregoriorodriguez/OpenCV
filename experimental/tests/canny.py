from __init__ import *

#Solo funciona con GrayScaleProcessor
visualizer = CamVisualizer(processors=[GrayScaleProcessor(),CannyProcessor()])
visualizer.show()
