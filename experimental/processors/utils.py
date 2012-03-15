from numpy import arange
import types

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class Trackbar:
    cls_name = None
    processor = None
    def __init__ (self,*args,**kwargs):
        self._name = kwargs.get('name',None)
        self.default = kwargs.get('default',0)
        self.values = kwargs['values'] if 'values' in kwargs else args[0] if isinstance(args[0], types.ListType) else arange(*args)
        self.instant = kwargs.get('instant')
        self.parent = None
        self._set_value(self.default)

    @property
    def max (self):
        return len(self.values)-1

    def _get_value (self):
        return self._value
    def _set_value (self,value):
        self._value = self.values[value]
        if self.instant and self.parent: self.parent.paint()
        self.log('Trackbar: %s = %s'%(self.name,str(self._value)))

    value = property(_get_value,_set_value)

    def _get_name (self):
        return '%s: %s' %(str(self.processor),self._name or self.cls_name)
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

