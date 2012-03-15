from . import Processor
import numpy as np

class FormatInt8(Processor):
    def process(self,img):
        return np.array(img,dtype = np.uint8)

class FormatFloat(Processor):
    def process(self,img):
        return np.array(img,dtype = float)
