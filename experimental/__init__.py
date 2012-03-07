from tests import *
from processors.filters import *

if __name__ == "__main__":
    #test = cam(combine(GrayScaleTest,GaussianBlurTest,ResizeComplexTrackbarTest))()
    # test = CamTest(processors=[PyrDownProcessor(),BlurProcessor(),SobelProcessor()])
    # test = CamTest(processors=[ResizeComplexTrackbarProcessor(),GaussianBlurProcessor()])
    #test = CamTest(processors=[PyrDownProcessor(),GaussianBlurProcessor(),SobelProcessor()])
    # test = ImageTest(
    #     file='../img/beach.jpg',
    #     processors=[PyrDownProcessor(),GaussianBlurProcessor(),SobelProcessor()])
    #test = CamTest(processors=[ResizeComplexTrackbarProcessor(),MedianBlurProcessor()])
    test = CamTest(processors=[GrayScaleProcessor(),PyrDownProcessor(),CannyProcessor(threshold1=600,threshold2=600)])
    test.show()
