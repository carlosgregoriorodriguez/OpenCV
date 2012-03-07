from __init__ import *

visualizer = CamVisualizer(processors=[ErodeProcessor(),DilateProcessor()])
visualizer.show()
