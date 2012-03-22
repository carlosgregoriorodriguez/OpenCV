#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

#TEST Match Template ...

import cv2
import numpy

def dummy(x):
    print x

if __name__ == "__main__":

    img = cv2.imread("../../img/triangles.jpg",0)        #load and show original
    cv2.imshow("ORIGINAL",img)
    tmp = cv2.imread("../../img/triangleTemplate.jpg",0) #load and show template
    cv2.imshow("TEMPLATE",tmp)

    cv2.namedWindow("matchings")                         #create window
    cv2.createTrackbar("mode","matchings",0,2,dummy)    #create trackbars
    cv2.createTrackbar("normed","matchings",0,1,dummy)
    modeDict = {0:{0:cv2.TM_CCORR , 1: cv2.TM_SQDIFF , 2: cv2.TM_CCOEFF},
                1:{0:cv2.TM_CCORR_NORMED , 1: cv2.TM_SQDIFF_NORMED 
                   , 2: cv2.TM_CCOEFF_NORMED}}

    while True:
        matchingMethod = modeDict[cv2.getTrackbarPos("normed","matchings")][cv2.getTrackbarPos("mode","matchings")]
        result = cv2.matchTemplate(img,tmp,method=matchingMethod)
        cv2.imshow("matchings",result)
        if (cv2.waitKey(5)!=-1):
            break

