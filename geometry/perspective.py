#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy

def onMouse (event, x, y, flags, param):
    global contp, p
    if flags & cv2.EVENT_FLAG_LBUTTON:
        if contp < 3:
            print (x,y)
            p[contp] = (x,y)
            contp = contp+1
            cv2.circle(img, (x,y), 3, (0,0,255), -1)
            cv2.imshow('image',img)
        elif contp == 3:
            print (x,y)
            p[contp] = (x,y)
            contp = 0
            cv2.circle(img, (x,y), 3, (0,0,255), -1)
            cv2.imshow('image',img)
            
            h = img.shape[0]
            w = img.shape[1]

            ori = numpy.zeros((4,2),numpy.float32)
            ori[0] = p[0]
            ori[1] = p[1]
            ori[2] = p[2]
            ori[3] = p[3]

            dest = numpy.zeros((4,2),numpy.float32)
            dest[0] = [0,0]
            dest[1] = [w,0]
            dest[2] = [0,h]
            dest[3] = [w,h]

            M = cv2.getPerspectiveTransform(ori,dest)
            img2 = cv2.warpPerspective(img, M, (w,h))

            cv2.imshow("image2",img2)

if __name__ == "__main__":

    img = cv2.imread(sys.argv[1])
    cv2.imshow("image",img)
    contp = 0
    p = [0,0,0,0]
    cv2.setMouseCallback("image",onMouse)
        

    cv2.waitKey(0)
