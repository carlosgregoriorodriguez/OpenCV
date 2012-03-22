import cv2
from . import Processor, Trackbar
import numpy as np

class CascadeClassifierProcessor(Processor):
    def __init__ (self,*args,**kwargs):
        xml = kwargs.pop('xml',None)
        if not xml: raise Exception('Cascade xml file missing')
        self.xml = xml
        super(CascadeClassifierProcessor,self).__init__(*args,**kwargs)
    def _set_xml(self,xml):
        self.classifier = cv2.CascadeClassifier(xml)
        self._xml = xml
    def _get_xml(self):
        return self._xml
    xml = property(_get_xml,_set_xml)
    def process(self,img):
        rects = self.classifier.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        if not len(rects): rects = []
        else: rects[:,2:] += rects[:,:2]
        self.log('Rects detected: %s'%str(rects))
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

        return img