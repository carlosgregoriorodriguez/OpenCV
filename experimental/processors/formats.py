from . import Processor
import numpy as np

def astype_inplace(a, dtype, blocksize=10000):
    oldtype = a.dtype
    newtype = np.dtype(dtype)
    assert oldtype.itemsize is newtype.itemsize
    for idx in xrange(0, a.size, blocksize):
        a.flat[idx:idx + blocksize] = \
            a.flat[idx:idx + blocksize].astype(newtype).view(oldtype)
    a.dtype = newtype
    
class FormatInt8(Processor):
    def process(self,img):
        return img.astype(np.uint8)

class FormatFloat(Processor):
    def process(self,img):
        return img.astype(float)
