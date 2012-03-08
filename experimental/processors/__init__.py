from utils import Struct, Trackbar

class MetaProcessor(type):
    def __new__(cls, name, bases, dct):
        trackbars = []
        for _name, value in dct.items():
            if isinstance(value,Trackbar):
                value.cls_name = _name
                trackbars.append(value)
        dct['meta'] = Struct(trackbars=trackbars)
        return type.__new__(cls, name, bases, dct)

class Processor(object):
    __metaclass__ = MetaProcessor
    def __init__ (self,**kwargs):
        self.meta.settings = kwargs
        for trackbar in self.meta.trackbars:
            trackbar.processor = self

    def contribute_to_test (self,test):
        keys = self.meta.settings.keys()
        for trackbar in self.meta.trackbars:
            key = trackbar.cls_name
            if key not in keys:
                test.add_trackbar(trackbar)
            else:
                trackbar._value = self.meta.settings[key]
    def process(self,img):
        return img 

    def __str__ (self):
        return self.__class__.__name__.lower().replace('processor','').capitalize()

class ProcessorMethod (Processor):
    method = None
    method_args = []
    method_kargs = {}
    def process(self,img):
        return self.method(img,*self.method_args,**self.method_kargs)
