import cv2
from . import Processor, Trackbar
import numpy as np

class HistogramProcessor(Processor):
    def process(self,img):
        h = np.zeros((300,255,3))
        b,g,r = cv2.split(img)
        bins = np.arange(256).reshape(256,1)
        color = [ (255,0,0),(0,255,0),(0,0,255) ]


        for item,col in zip([b,g,r],color):
            hist_item = cv2.calcHist([item],[0],None,[256],[0,255])

            cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)

            hist=np.int32(np.around(hist_item))

            pts = np.column_stack((bins,hist))

            cv2.polylines(h,np.array([pts],np.int32),False,col)

        return np.flipud(h)


class HistogramDistanceProcessor(Processor):
    last_histogram = None
    type = Trackbar([cv2.cv.CV_COMP_CORREL,cv2.cv.CV_COMP_CHISQR,cv2.cv.CV_COMP_INTERSECT,cv2.cv.CV_COMP_BHATTACHARYYA])
    normalize = {
        cv2.cv.CV_COMP_CORREL: lambda x:1-x,
        cv2.cv.CV_COMP_CHISQR: lambda x: x/10,
        cv2.cv.CV_COMP_INTERSECT: lambda x: x,
        cv2.cv.CV_COMP_BHATTACHARYYA: lambda x: x,        
    }
    def process(self,img):
        img = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)
        histogram = cv2.calcHist([img],[0],None,[256],[0,255]) 
        cv2.normalize(histogram,histogram,0,255,cv2.NORM_MINMAX)

        if self.last_histogram!=None:
            distance = cv2.compareHist(self.last_histogram,histogram,self.type.value)
            self.log('Distance (%d) is %f'%(self.type.value,distance))
            norm = self.normalize[self.type.value](distance)
            norm = max(min(norm,1),0)
            radius = int((norm**0.5)*20)
            cv2.ellipse(img, (20, 20),  (radius,radius), 0, 0, 360, 255, -1 );

        self.last_histogram = histogram
        return img