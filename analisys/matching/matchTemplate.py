#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

#TEST Match Template ...

import cv2
import numpy

if __name__ == "__main__":

    img = cv2.imread("../../img/triangles.jpg",0)
    cv2.imshow("ORIGINAL",img)
    tmp = cv2.imread("../../img/triangleTemplate.jpg",0)
    cv2.imshow("TEMPLATE",tmp)

    result1 = cv2.matchTemplate(img,tmp,method=cv2.TM_CCORR)
    #print "CCORR"
    #print result1
    cv2.imshow("matchings CCORR",result1)

    #result1a = cv2.matchTemplate(img,tmp,method=cv2.TM_CCORR_NORMED)
    #print "NORMED"
    #print result1a
    #cv2.imshow("matchings CCORR_NORMED",result1a)

    result2 = cv2.matchTemplate(img,tmp,method=cv2.TM_SQDIFF)
    cv2.imshow("matchings SQDIFF",result2)

    result3 = cv2.matchTemplate(img,tmp,method=cv2.TM_CCOEFF)
    cv2.imshow("matchings CCOEFF",result3)

    cv2.waitKey(0)
