import cv2
from . import Processor, Trackbar
# import numpy as np
from filters import GrayScaleProcessor

#Doesn't work at all

class GoodFeaturesProcessor(GrayScaleProcessor):
    num = Trackbar(100,default=5)
    distance = Trackbar(1,250)
    quality = Trackbar(0,1,0.01)
    type = Trackbar([cv2.THRESH_BINARY,cv2.THRESH_BINARY_INV,cv2.THRESH_TRUNC,cv2.THRESH_TOZERO,cv2.THRESH_TOZERO_INV])
    def process(self,img):
        img = super(GoodFeaturesProcessor,self).process(img)
        corners = cv2.goodFeaturesToTrack(img,int(self.num),int(self.distance),float(self.quality))
        if corners:
            for c in corners:
                cv2.ellipse(img, (c[0][0], c[0][1]),  (5,5), 0, 0, 360, 255, -1 );
        return img
