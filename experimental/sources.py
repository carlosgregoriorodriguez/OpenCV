import cv2

class Source(object):
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
            if (cv2.waitKey (1) != -1):
                break

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
        super(VideoSource,self).__init__(*args,**kwargs)
    def get_source (self):
        return self.capture.read()[1]


class CamSource (VideoSource):
    def __init__(self,*args,**kwargs):
        kwargs['file'] = kwargs.get('device',0)
        super(CamSource,self).__init__(*args,**kwargs)


