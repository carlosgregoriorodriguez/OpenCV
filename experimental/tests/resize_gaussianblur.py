from __init__ import *

#test = cam(combine(GrayScaleTest,GaussianBlurTest,ResizeComplexTrackbarTest))()
# test = CamTest(processors=[PyrDownProcessor(),BlurProcessor(),SobelProcessor()])
visualizer = CamVisualizer(processors=[ResizeComplexTrackbarProcessor(),GaussianBlurProcessor()])
#test = CamTest(processors=[PyrDownProcessor(),GaussianBlurProcessor(),SobelProcessor()])
# test = ImageTest(
#     file='../img/beach.jpg',
#     processors=[PyrDownProcessor(),GaussianBlurProcessor(),SobelProcessor()])
#test = CamTest(processors=[ResizeComplexTrackbarProcessor(),MedianBlurProcessor()])
# test = CamTest(processors=[GrayScaleProcessor(),PyrDownProcessor(),CannyProcessor(threshold1=600,threshold2=600)])
visualizer.show()
