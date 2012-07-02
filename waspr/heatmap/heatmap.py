from PIL import Image,ImageChops
import math
import tempfile
import numpy as np
import os

class Point(object):
    """Point class with public x and y attributes """
 
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def dist(self, p):
        """return the Euclidian distance between self and p"""
        dx = self.x - p.x
        dy = self.y - p.y
        return math.sqrt(dx**2 + dy**2)
 
    def reset(self):
        self.x = 0
        self.y = 0

    def __add__(self, p):
        """return a new point found by adding self and p. This method is
        called by e.g. p+q for points p and q"""
        return Point(self.x+p.x, self.y+p.y)

    def __sub__(self, p):
        """return a new point found by substracting self and p. This method is
        called by e.g. p-q for points p and q"""
        return Point(self.x-p.x, self.y-p.y)

    def __pow__(self, p):
        """return a new point found by adding self and p. This method is
        called by e.g. p**q for points p and q"""
        return (self.x**p+self.y**p)**(1/p)
 
    def __repr__(self):
        """return a string representation of this point. This method is
        called by the repr() function, and
        also the str() function. It should produce a string that, when
        evaluated, returns a point with the 
        same data."""
        return 'Point(%d,%d)' % (self.x, self.y)


class Heatmap(object):
    max = -1
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.map = np.ndarray((width,height),np.float)
        self.load_palette()

    @property
    def size(self):
        return self.width,self.height
    

    def addPoint(self,point,radius=5):
        a1 = range(max(point.x-radius,0),min(point.x+radius,self.width))
        a2 = range(max(point.y-radius,0),min(point.y+radius,self.height))
        for x in a1:
            for y in a2:
                # d = point.dist(Point(x,y))
                d = math.sqrt((point.x-x)**2 + (point.y-y)**2)
                if d>radius: continue
                self.map[x,y] = self.map[x,y]+((0.5 + math.cos(d * math.pi / radius) * 0.5) * 0.05)
                if self.map[x,y]>1: self.map[x,y]=1
                if self.map[x,y]>self.max:self.max = self.map[x,y]

    def load_palette(self,path=None):
        path = path or os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),'palettes/classic.png')
        im = Image.open(path)
        self.palette = []
        h = im.size[1]
        for i in xrange(h):
            r,g,b = im.getpixel((0,h-i-1))
            self.palette.append((((((255<<8)+b)<<8)+g)<<8)+r)
        #print self.palette

    def transform(self):
        return  (255-self.map * 255).round()

        l = len(self.palette)-1
        mm = self.max if self.max >1 else 1
        def _formatPixel(m):
            # if m<=0: return 0xffffffff
            m /= mm
            # if m>1:m=1.
            return self.palette[int((m**0.8)*l)]
            #return (((((a<<8)+b)<<8)+g)<<8)+r

        print 'a'
        _formatPixel = np.vectorize(_formatPixel)
        #c = np.zeros((100, 100), np.uint32)
        #c[:,:] = 0xff808000
        print 'b'
        #data = np.array(_formatPixel(self.map), np.uint32) # np.array([_formatPixel(d) for d in self.map.flat], np.uint32).reshape(self.map.shape) # 
        print 'c'
        #data = np.transpose(self.map)
        print 'd'
        img8 = (255-self.map * 255).round()
        #np.transpose(img8)
        return img8
        img = Image.fromarray(img8)
        #img =  Image.frombuffer('RGBA', (self.width, self.height), np.transpose(img8), 'raw', 'RGBA', 0, 1)
        # Image.fromstring(mode, (a.shape[1], a.shape[0]), a.tostring())
        return img


def preview(img):
    import webbrowser
    f = tempfile.NamedTemporaryFile(suffix='.png',delete=False)
    img.save(f,'png')
    webbrowser.open('file://'+f.name)


if __name__ == '__main__':
    hm = Heatmap(1000,1000)
    #hm.load_palette('palettes/classic.png')
    hm.addPoint(Point(50,50),20)
    hm.addPoint(Point(50,50),20)
    img = hm.transform()
    preview(img)
    hm.addPoint(Point(10,50),20)
    img = hm.transform()
    preview(img)
    #f.close()
