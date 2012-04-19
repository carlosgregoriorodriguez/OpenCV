from utils import Struct, Trackbar
from copy import copy

class MetaProcessor(type):
    def __new__(cls, name, bases, dct):
        trackbars = []
        for _name, value in dct.items():
            if isinstance(value,Trackbar):
                #v = deepcopy(value)
                #print _name,v
                value.cls_name = _name
                trackbars.append(value)
                del dct[_name]
        dct['meta'] = Struct(trackbars=trackbars)
        return type.__new__(cls, name, bases, dct)

class Processor(object):
    __metaclass__ = MetaProcessor
    def __init__ (self,**kwargs):
        self.settings = kwargs
        for trackbar in self.meta.trackbars:
            t = copy(trackbar)
            setattr(self,trackbar.cls_name,t)
            t.processor = self

    def contribute_to_test (self,test):
        keys = self.settings.keys()
        self.parent = test
        for trackbar in self.meta.trackbars:
            key = trackbar.cls_name
            t = getattr(self,key)
            #print repr(self),key, t
            if key not in keys:
                test.add_trackbar(t)
            else:
                # print 'default value',self.settings[key]
                t._value = self.settings[key]
    def process(self,img):
        return img 

    def on_mouse(self,*args,**kwargs):
        pass

    def on_key(self,key):
        pass

    def paint(self):
        self.parent.paint()

    def log(self,*args,**kwargs):
        self.parent and self.parent.log(*args,**kwargs)

    def __str__ (self):
        return self.__class__.__name__.lower().replace('processor','').capitalize()

import types

def processor(*args,**kwargs):
    if args:
        func = args[0]
        processors = args[1:]
    else:
        func = None
        processors = tuple()
    # def process(self,*args,**kwargs):
    #     return func(*args,**kwargs)
    final = not kwargs and (type(func)==types.FunctionType or type(func)==types.MethodType)

    if not final and func: processors = (func,)+processors
    # processors += 
    def dec(f):
        def process(self,img):
            img = super(c,self).process(img)
            trackbar_values = dict([(t.cls_name,getattr(self,t.cls_name).value) for t in self.meta.trackbars]) if f != func else {}
            return f(img,**trackbar_values)

        # print kwargs
        # class prueba(processors or Processor):
        #     def process(self,img):
        #         img = super(prueba,self).process(img)
        #         return func(img)
        # return prueba
        kwargs['process'] = process 
        c =  type(f.func_name, processors or (Processor,), kwargs)
        return c
    return dec(func) if final else dec
        

class ProcessorMethod (Processor):
    method = None
    method_args = []
    method_kargs = {}
    def process(self,img):
        return self.method(img,*self.method_args,**self.method_kargs)
