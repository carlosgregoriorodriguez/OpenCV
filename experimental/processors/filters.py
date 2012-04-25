import cv2
from . import Processor, ProcessorMethod, Trackbar
import numpy as np
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

class BorderProcessor(Processor):
    type = Trackbar([cv2.BORDER_DEFAULT,cv2.BORDER_CONSTANT,cv2.BORDER_WRAP,cv2.BORDER_REFLECT_101])
    length = Trackbar(100,default=50)
    def process(self,img):
        l = int(self.length)
        return cv2.copyMakeBorder(img,l,l,l,l,int(self.type))

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
    iterations = Trackbar(50)
    def process(self,img):
        print 'a',self,self.__class__.__bases__
        return cv2.erode(img,kernel=None,iterations=int(self.iterations))

class DilateProcessor(Processor):
    iterations = Trackbar(50)
    def process(self,img):
        return cv2.dilate(img,kernel=None,iterations=int(self.iterations))

class LaplacianProcessor(Processor):
    laplacian = Trackbar([0,5])
    def process(self,img):
        return cv2.Laplacian(img,int(self.laplacian))

class SobelProcessor(Processor):
    ddepth = Trackbar([0,5],default=1)
    dx = Trackbar(3)
    dy = Trackbar(3,default=1)
    #ksize = Trackbar(default=0,values=[1,3,5,7])
    def process(self,img):
        #kx,ky = cv2.getDerivKernels(self.dx, self.dy, self.ksize)
        return cv2.Sobel(img,int(self.ddepth),int(self.dx),int(self.dy))

class MeanShiftFilteringProcessor(Processor):
    spatial_radius = Trackbar(12)
    color_radius = Trackbar(12)
    def process(self,img):
        return cv2.pyrMeanShiftFiltering(img,int(self.spatial_radius),int(self.color_radius)) #int(self.dx),int(self.dy)

class BoxFilterProcessor(Processor):
    ksize_x = Trackbar(1,200)
    ksize_y = Trackbar(1,200)
    def process(self,img):
        return cv2.boxFilter(img,-1,(int(self.ksize_x),int(self.ksize_y)))

class CannyProcessor(GrayScaleProcessor):
    threshold1 = Trackbar(600,default=200)
    threshold2 = Trackbar(600,default=80)
    aperture = Trackbar([3,5,7])
    def process(self,img):
        img = super(CannyProcessor,self).process(img)
        return cv2.Canny(img,threshold1=int(self.threshold1),threshold2=int(self.threshold2),apertureSize=int(self.aperture))


class ThresholdProcessor(Processor):
    thresh = Trackbar(256,default=60)
    maxval = Trackbar(256,default=160)
    type = Trackbar([cv2.THRESH_BINARY,cv2.THRESH_BINARY_INV,cv2.THRESH_TRUNC,cv2.THRESH_TOZERO,cv2.THRESH_TOZERO_INV])
    def process(self,img):
        retVal, newimg = cv2.threshold(img,int(self.thresh),int(self.maxval),self.type.value)
        return newimg

class AdaptiveThresholdProcessor(GrayScaleProcessor):
    method = Trackbar([cv2.ADAPTIVE_THRESH_MEAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C])
    maxval = Trackbar(1,256,default=160)
    type = Trackbar([cv2.THRESH_BINARY,cv2.THRESH_BINARY_INV])
    blockSize = Trackbar(3,20,2,default=3)
    def process(self,img):
        img = super(AdaptiveThresholdProcessor,self).process(img)
        return cv2.adaptiveThreshold(img, self.maxval.value, self.method.value, self.type.value, self.blockSize.value, 5) 

class FloodFillProcessor(Processor):
    hi = Trackbar(256,default=6)
    lo = Trackbar(256,default=12)
    connectivity = Trackbar([4,8],default=0)
    seed_pt = None

    def process(self,img):
        h, w = img.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        cv2.floodFill(img, mask, self.seed_pt, (255, 255, 255), (int(self.lo),)*3, (int(self.hi),)*3, int(self.connectivity))
        cv2.circle(img, self.seed_pt, 3, (0, 0, 255), -1)
        return img

    def on_mouse(self,event, x, y, flags, param):
        if flags == cv2.EVENT_FLAG_LBUTTON:
            self.seed_pt = x, y
            self.paint()
