from PIL import Image,ImageChops
import math
import tempfile
import numpy as np
class Point(object):
    """Point class with public x and y attributes """
 
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def dist(self, p):
        """return the Euclidian distance between self and p"""
        dx = self.x - p.x
        dy = self.y - p.y
        return math.sqrt(dx*dx + dy*dy)
 
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
    max = 0
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.map = np.empty((width,height),np.float32)


    @property
    def size(self):
        return self.width,self.height
    

    def addPoint(self,point,radius=5):
        for x in xrange(max(point.x-radius,0),min(point.x+radius,self.width)):
            for y in xrange(max(point.y-radius,0),min(point.y+radius,self.height)):
                d = point.dist(Point(x,y))
                if d>radius: continue
                self.map[x,y] += ((0.5 + math.cos(d * math.pi / radius) * 0.5) * 0.25)
                if self.map[x,y]>self.max: self.max = self.map[x,y]

    def transform(self,palette):
        def _formatPixel(m):
            return (255,255,255,255)
        _formatPixel = np.vectorize(_formatPixel)
        img =  Image.fromarray(_formatPixel(self.map), "RGBA")
        # Image.fromstring(mode, (a.shape[1], a.shape[0]), a.tostring())
        return img

import webbrowser


if __name__ == '__main__':
    hm = Heatmap(100,100)
    hm.addPoint(Point(50,50),20)
    img = hm.transform('')
    f = tempfile.NamedTemporaryFile(suffix='.png',delete=False)
    img.save(f,'png')
    webbrowser.open('file://'+f.name)
    #f.close()
