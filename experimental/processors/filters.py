import cv2
from . import Processor, ProcessorMethod, Trackbar
# is_odd = lambda x: x%2!=0 
# is_even = lambda x: x%2==0 
# def odd (l):
#     return list(filter(is_odd,l))
# def even (l):
#     return list(filter(is_even,l))

class PyrDownProcessor(ProcessorMethod):
    method = cv2.pyrDown

class PyrUpProcessor(ProcessorMethod):
    method = cv2.pyrUp

class ResizeProcessor(ProcessorMethod):
    method = cv2.resize
    method_args = ((200,200),)

class ResizeComplexProcessor(Processor):
    resize_value = 0.5
    def process(self,img):
        new_imgShape = map(lambda x: int(x*float(self.resize_value)),img.shape[1::-1])
        return cv2.resize(img,tuple(new_imgShape))

class ResizeComplexTrackbarProcessor(ResizeComplexProcessor):
    resize_value = Trackbar(.1,2,.1,instant=False)


class BlurProcessor(Processor):
    blur = Trackbar(1,30)
    def process(self,img):
        return cv2.blur(img,(int(self.blur),)*2)

class MedianBlurProcessor(Processor):
    blur = Trackbar(3,10,2)
    def process(self,img):
        return cv2.medianBlur(img,int(self.blur))

class GaussianBlurProcessor(Processor):
    blur = Trackbar(3,10,2)
    sigma = Trackbar(10)
    def process(self,img):
        return cv2.GaussianBlur(img,(int(self.blur),)*2,float(self.sigma))

class GrayScaleProcessor (Processor):
    def process(self,img):
        return cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

class ErodeProcessor(Processor):
    erode = Trackbar(1)
    def process(self,img):
        return cv2.erode(img,kernel=0,iterations=2)

class LaplacianProcessor(Processor):
    laplacian = Trackbar(100)
    def process(self,img):
        return cv2.Laplacian(img,int(self.laplacian))

class SobelProcessor(Processor):
    ddepth = Trackbar([0,5])
    dx = Trackbar(2)
    dy = Trackbar(2)
    #ksize = Trackbar(default=0,values=[1,3,5,7])
    def process(self,img):
        #kx,ky = cv2.getDerivKernels(self.dx, self.dy, self.ksize)
        return cv2.Sobel(img,int(self.ddepth),int(self.dx),int(self.dy))

class MeanShiftFilteringProcessor(Processor):
    spatial_radius = Trackbar(12)
    color_radius = Trackbar(12)
    def process(self,img):
        return cv2.pyrMeanShiftFiltering(img,int(self.spatial_radius),int(self.color_radius)) #int(self.dx),int(self.dy)

class CannyProcessor(Processor):
    threshold1 = Trackbar(600,default=200)
    threshold2 = Trackbar(600,default=80)
    aperture = Trackbar([3,5,7])
    def process(self,img):
        return cv2.Canny(img,threshold1=int(self.threshold1),threshold2=int(self.threshold2),apertureSize=int(self.aperture))

