from __init__ import *

visualizer = CamSource(
  	Window(processors=[
  		CascadeClassifierProcessor(xml='../data/objdetect/face.xml'),
  		CascadeClassifierProcessor(xml='../data/objdetect/eye.xml'),
  	])
)
visualizer.show()
