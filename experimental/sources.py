import cv2

class Source(object):
    quit_keys = (27,113)
    def __init__(self,*windows):
        self.windows = windows

    def show (self):
        for window in self.windows:
            window.show()

    def paint(self):
        img = self.get_source()
        for window in self.windows:
            window.paint(img)

    def get_source (self):
        return


class FramedSource (Source):
    def show (self):
        super(FramedSource,self).show()
        while True:
            self.paint()
            key = cv2.waitKey (1)
            self.on_key(key)
            if key in self.quit_keys:
                break

    def on_key(self,key):
        for window in self.windows:
            window.on_key(key)

    def get_source (self):
        return

class ImageSource (Source):
    def __init__(self,*args,**kwargs):
        file = kwargs.pop('file',0)
        self.img = cv2.imread(file)
        super(ImageSource,self).__init__(*args,**kwargs)
    
    def show(self):
        super(ImageSource,self).show()
        self.paint()
        cv2.waitKey(0)

    def get_source (self):
        return self.img

class VideoSource (FramedSource):
    def __init__(self,*args,**kwargs):
        file = kwargs.pop('file')
        self.capture = cv2.VideoCapture(file)
        self.width = kwargs.pop('width',640)
        self.height = kwargs.pop('height',480)
        super(VideoSource,self).__init__(*args,**kwargs)
    def _set_width (self,width):
        self._width = width
        self.capture.set(3,width)
    def _get_width (self):
        return self._width
    width = property(_get_width, _set_width)
    def _set_height (self,height):
        self._height = height
        self.capture.set(4,height)
    def _get_height (self):
        return self._height
    height = property(_get_width, _set_height)
    def get_source (self):
        return self.capture.read()[1]


class CamSource (VideoSource):
    def __init__(self,*args,**kwargs):
        kwargs['file'] = kwargs.get('device',0)
        super(CamSource,self).__init__(*args,**kwargs)

from window import Window
def view(source,*processors):
    visualizer = source(
      Window(processors=processors)
    )
    visualizer.show()
    return visualizer

def camview(*processors): return view(CamSource, *processors)
