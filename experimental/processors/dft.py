import cv2
from . import Processor, Trackbar
import numpy as np

class DFTProcessor(Processor):
    inverse = cv2.DFT_INVERSE
    scale = cv2.DFT_SCALE
    invs = inverse+scale
    flags = Trackbar([0, inverse, scale, invs])
    def process(self,img):
        img = img.astype(float)
        extra = {}
        if self.flags.value!=None: extra['flags'] = self.flags.value
        img = cv2.dft(img,**extra)
        return img

class DCTProcessor(Processor):
    inverse = cv2.DCT_INVERSE
    flags = Trackbar([None, inverse])
    def process(self,img):
        img = img.astype(float)
        #img.dtype = np.float
        extra = {}
        if self.flags.value!=None: extra['flags'] = self.flags.value
        img = cv2.dct(img,**extra)
        #img.dtype = np.uint8
        return img
