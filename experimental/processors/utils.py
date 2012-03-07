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
