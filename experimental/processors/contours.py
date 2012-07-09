import cv2
from . import Processor, Trackbar

class ContoursProcessor(Processor):
    distance = Trackbar(1,15)
    level = Trackbar(1,10)
    type = Trackbar([cv2.cv.CV_RETR_EXTERNAL, cv2.cv.CV_RETR_LIST, cv2.cv.CV_RETR_CCOMP, cv2.cv.CV_RETR_TREE])
    def process(self,img):
    	bimg = img.copy()
        raw_contours, hierarchy = cv2.findContours(bimg, self.type.value, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cv2.approxPolyDP(c, self.distance.value, True) for c in raw_contours]
        cv2.drawContours(bimg, contours, -1, (0,0,0), 2, cv2.CV_AA, hierarchy, int(self.level))
        cv2.drawContours(bimg, contours, -1, (255,255,255), 1, cv2.CV_AA, hierarchy, int(self.level))
        return bimg