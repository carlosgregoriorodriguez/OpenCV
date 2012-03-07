#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import time

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)


class Trackbar:
    cls_name = None
    def __init__ (self,name=None,default=0,max=10,processor=lambda x:x,values=[]):
        self._name = name
        self.default = default
        self.max = max
        if values:
            self.max = len(values)-1
            processor = lambda x:values[x]
        self.processor = processor
        self.parent = None
        self._set_value(default)
    def _get_value (self):
        return self._value
    def _set_value (self,value):
        self._value = self.processor(value)
        if self.parent: self.parent.paint()
        self.log('Trackbar %s changed to %g'%(self.name,self._value))

    value = property(_get_value,_set_value)

    def _get_name (self):
        return self._name or self.cls_name
    def _set_name (self,name):
        self._name = name
    name = property(_get_name,_set_name)

    def log(self,*args,**kwargs):
        self.parent and self.parent.log(*args,**kwargs)

    @property
    def window_name(self):
        return self.parent.window_name

    def __float__ (self):
        return float(self.value)
    def __int__ (self):
        return int(self.value)



class Test(object):
    _window_name = None
    parent = None
    def __init__(self, debug=True, processors=[]):
        self.debug = debug
        self.processors = processors
        self.log('Init capture')

    def add_trackbar(self,trackbar):
        trackbar.parent = self if not self.parent else self.parent
        cv2.createTrackbar(trackbar.name,trackbar.window_name,trackbar.default,trackbar.max,trackbar._set_value)

    def log (self,message):
        if self.debug: print '%s: %s'%(self.window_name,message)

    def get_source (self):
        return None

    def _set_window_name (self,name):
        self._window_name = name

    def _get_window_name(self):
        return self._window_name if self._window_name else self.__class__.__name__

    window_name = property(_get_window_name,_set_window_name)

    def show(self):
        cv2.namedWindow(self.window_name)
        for processor in self.processors:
            processor.contribute_to_test(self)

    def paint (self):
        img = self.get_source()
        try:
            before = time.time()
            for processor in self.processors:
                img = processor.process(img)
            fps = 1/(time.time()-before)
            if self.debug:
                cv2.putText(img=img, text="%d fps"%fps, org=(20, 20), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                    color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)        
                cv2.putText(img=img, text="%d fps"%fps, org=(20, 20), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                    color=(255, 255, 255), thickness = 1, linetype=cv2.CV_AA)        

        except Exception, e:
            img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
            cv2.putText(img=img, text="Error", org=(20, 30), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, 
                    color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)        
            cv2.putText(img=img, text="Error", org=(20, 30), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, 
                    color=(0, 0, 255), thickness = 1, linetype=cv2.CV_AA)        

            self.log('Exception ocurred: %s'%str(e))

        cv2.imshow(self.window_name,img)

class FramedTest (Test):
    def show (self):
        super(FramedTest,self).show()
        while True:
            self.paint()
            if (cv2.waitKey (1) != -1):
                break

    def get_source (self):
        return

class ImageTest (Test):
    def __init__(self,*args,**kwargs):
        file = kwargs.pop('file',0)
        self.img = cv2.imread(file)
        super(ImageTest,self).__init__(*args,**kwargs)
    
    def show(self):
        super(ImageTest,self).show()
        self.paint()
        cv2.waitKey(0)

    def get_source (self):
        return self.img

class VideoTest (FramedTest):
    def __init__(self,*args,**kwargs):
        file = kwargs.pop('file')
        self.capture = cv2.VideoCapture(file)
        super(VideoTest,self).__init__(*args,**kwargs)
    def get_source (self):
        return self.capture.read()[1]


class CamTest (VideoTest):
    def __init__(self,*args,**kwargs):
        kwargs['file'] = kwargs.get('device',0)
        super(CamTest,self).__init__(*args,**kwargs)

class MetaProcessor(type):
    def __new__(cls, name, bases, dct):
        #trackbars = (name for name, value in dct.items() if isinstance(value,Trackbar))
        #(not name.startswith('__')) and 
        trackbars = []
        for _name, value in dct.items():
            if isinstance(value,Trackbar):
                value.cls_name = _name
                trackbars.append(value)
        dct['meta'] = Struct(trackbars=trackbars)
        return type.__new__(cls, name, bases, dct)

class Processor(object):
    __metaclass__ = MetaProcessor
    def contribute_to_test (self,test):
        for trackbar in self.meta.trackbars:
            test.add_trackbar(trackbar)
    def process(self,img):
        return img 

class ProcessorMethod (Processor):
    method = None
    method_args = []
    method_kargs = {}
    def process(self,img):
        return self.method(img,*self.method_args,**self.method_kargs)


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
    resize_value = Trackbar(default=1,processor=lambda x:(x+1)/5.0)


class BlurProcessor(Processor):
    blur = Trackbar(default=0,max=30,processor=lambda x:x+1)
    def process(self,img):
        return cv2.blur(img,(int(self.blur),)*2)

class MedianBlurProcessor(Processor):
    blur = Trackbar(default=0,max=10,processor=lambda x:2*x+3)
    def process(self,img):
        return cv2.medianBlur(img,int(self.blur))

class GaussianBlurProcessor(Processor):
    blur = Trackbar(default=0,max=10,processor=lambda x:2*x+3)
    sigma = Trackbar(default=0,max=10)
    def process(self,img):
        return cv2.GaussianBlur(img,(int(self.blur),)*2,float(self.sigma))

class GrayScaleProcessor (Processor):
    def process(self,img):
        return cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

class ErodeProcessor(Processor):
    erode = Trackbar(default=0,max=1)
    def process(self,img):
        return cv2.erode(img,kernel=0,iterations=2)

class LaplacianProcessor(Processor):
    laplacian = Trackbar(default=0,max=100)
    def process(self,img):
        return cv2.Laplacian(img,int(self.laplacian))

class SobelProcessor(Processor):
    ddepth = Trackbar(default=0,values=[0,5])
    dx = Trackbar(default=0,max=2)
    dy = Trackbar(default=1,max=2)
    #ksize = Trackbar(default=0,values=[1,3,5,7])
    def process(self,img):
        #kx,ky = cv2.getDerivKernels(self.dx, self.dy, self.ksize)
        return cv2.Sobel(img,int(self.ddepth),int(self.dx),int(self.dy))

class MeanShiftFilteringProcessor(Processor):
    spatial_radius = Trackbar(default=0,max=12)
    color_radius = Trackbar(default=0,max=12)
    def process(self,img):
        return cv2.pyrMeanShiftFiltering(img,int(self.spatial_radius),int(self.color_radius)) #int(self.dx),int(self.dy)

class CannyProcessor(Processor):
    threshold1 = Trackbar(default=200,max=600)
    threshold2 = Trackbar(default=80,max=600)
    aperture = Trackbar(default=0,values=[3,5,7])
    def process(self,img):
        return cv2.Canny(img,threshold1=int(self.threshold1),threshold2=int(self.threshold2),apertureSize=int(self.aperture))

import numpy as np

class HistogramProcessor(Processor):
    bins = np.arange(256).reshape(256,1)
    color = [ (255,0,0),(0,255,0),(0,0,255) ]
    def process(self,img):
        h = np.zeros((300,256,3))
        for ch, col in enumerate(self.color):
            hist_item = cv2.calcHist([img],[ch],None,[256],[0,255])
            cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
            hist=np.int32(np.around(hist_item))
            pts = np.column_stack((self.bins,hist))
            cv2.polylines(h,[pts],False,col)
        return np.flipud(h)




if __name__ == "__main__":
    #test = cam(combine(GrayScaleTest,GaussianBlurTest,ResizeComplexTrackbarTest))()
    #test = CamTest(processors=[PyrDownProcessor(),SobelProcessor()])
    #test = CamTest(processors=[PyrDownProcessor(),GaussianBlurProcessor(),SobelProcessor()])
    # test = ImageTest(
    #     file='../img/beach.jpg',
    #     processors=[PyrDownProcessor(),GaussianBlurProcessor(),SobelProcessor()])
    test = CamTest(processors=[ResizeComplexTrackbarProcessor(),MedianBlurProcessor()])
    #test = CamTest(processors=[GrayScaleProcessor(),PyrDownProcessor(),CannyProcessor()])
    test.show()
