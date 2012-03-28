import cv2
from . import Processor, Trackbar
import numpy as np
from filters import GrayScaleProcessor

def anorm2(a):
    return (a*a).sum(-1)
def anorm(a):
    return np.sqrt( anorm2(a) )

class CascadeClassifierProcessor(Processor):
    def __init__ (self,*args,**kwargs):
        xml = kwargs.pop('xml',None)
        if not xml: raise Exception('Cascade xml file missing')
        
        self.xml = xml
        super(CascadeClassifierProcessor,self).__init__(*args,**kwargs)
    
    def _set_xml(self,xml):
        self.classifier = cv2.CascadeClassifier(xml)
        self._xml = xml
    
    def _get_xml(self):
        return self._xml
    
    xml = property(_get_xml,_set_xml)
    
    def process(self,img):
        rects = self.classifier.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        
        if not len(rects): rects = []
        else: rects[:,2:] += rects[:,:2]
        
        self.log('Rects detected: %s'%str(rects))
        
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

        return img


def match_flann(desc1, desc2, r_threshold = 0.6):
    FLANN_INDEX_KDTREE = 1 
    flann = cv2.flann_Index(desc2, dict(algorithm = FLANN_INDEX_KDTREE, trees = 4))
    idx2, dist = flann.knnSearch(desc1, 2, params = {}) # bug: need to provide empty dict
    mask = dist[:,0] / dist[:,1] < r_threshold
    idx1 = np.arange(len(desc1))
    pairs = np.int32( zip(idx1, idx2[:,0]) )
    return pairs[mask]

def match_bruteforce(desc1, desc2, r_threshold = 0.75):
    res = []
    for i in xrange(len(desc1)):
        dist = anorm( desc2 - desc1[i] )
        n1, n2 = dist.argsort()[:2]
        r = dist[n1] / dist[n2]
        if r < r_threshold:
            res.append((i, n1))
    return np.array(res)

class SurfProcessor(GrayScaleProcessor):
    surf = cv2.SURF(3000,4,2,False,False)
    capturedImg = None
    rectSize = (240,320)
    _capture = False
    threshold = Trackbar(0.1,1,.1,default=8)
    homo_method = Trackbar([0,cv2.RANSAC,cv2.LMEDS],default=2)
    homo_ransac_thrs = Trackbar(1,10,default=8)
    
    def _set_capture(self,capture):
        self._capture = capture
    
    def _get_capture(self):
        c, self._capture = self._capture, False
        return c
    
    capture = property(_get_capture,_set_capture)


    def draw_match(self,img1, img2, p1, p2, status = None, H = None):
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        vis = np.zeros((max(h1, h2), w1+w2), np.uint8)
        vis[:h1, :w1] = img1
        vis[:h2, w1:w1+w2] = img2
        vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

        if H is not None:
            corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
            corners = np.int32( cv2.perspectiveTransform(corners.reshape(1, -1, 2), H).reshape(-1, 2) + (w1, 0) )
            cv2.polylines(vis, [corners], True, (255, 0, 0),thickness=2)
        
        if status is None:
            status = np.ones(len(p1), np.bool_)
        green = (0, 255, 0)
        red = (0, 0, 255)
        for (x1, y1), (x2, y2), inlier in zip(np.int32(p1), np.int32(p2), status):
            col = [red, green][inlier]
            if inlier:
                cv2.line(vis, (x1, y1), (x2+w1, y2), col)
                cv2.circle(vis, (x1, y1), 2, col, -1)
                cv2.circle(vis, (x2+w1, y2), 2, col, -1)
            else:
                r = 2
                thickness = 3
                cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
                cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
                cv2.line(vis, (x2+w1-r, y2-r), (x2+w1+r, y2+r), col, thickness)
                cv2.line(vis, (x2+w1-r, y2+r), (x2+w1+r, y2-r), col, thickness)
        return vis


    match_method = Trackbar([match_flann,match_bruteforce])
    def on_key(self,key):
        if key==32: self.capture = True
        elif key==13 or key==10: self.capturedImg = None

    def process(self,img):
        img_gray = super(SurfProcessor,self).process(img)
        cx,cy = int(img.shape[1]/2),int(img.shape[0]/2)
        cv2.rectangle(img,(cx-self.rectSize[0]/2,cy-self.rectSize[1]/2),(cx+self.rectSize[0]/2,cy+self.rectSize[1]/2),255)
        if self.capture:
            self.capturedImg = img_gray[cy-self.rectSize[1]/2:cy+self.rectSize[1]/2,cx-self.rectSize[0]/2:cx+self.rectSize[0]/2]
        if self.capturedImg!=None:
            kp1, desc1 = self.surf.detect(self.capturedImg, None, False)
            kp2, desc2 = self.surf.detect(img_gray, None, False)
            desc1.shape = (-1, self.surf.descriptorSize())
            desc2.shape = (-1, self.surf.descriptorSize())
            m = self.match_method.value(desc1, desc2, self.threshold.value)
            matched_p1 = np.array([kp1[i].pt for i, j in m])
            matched_p2 = np.array([kp2[j].pt for i, j in m])
            if len(matched_p1) >= 4 :
                H, status = cv2.findHomography(matched_p1, matched_p2, self.homo_method.value , self.homo_ransac_thrs.value) # cv2.LMEDS
            else:
                H, status = None, None
            return self.draw_match(self.capturedImg, img_gray, matched_p1, matched_p2, status, H)
        return img