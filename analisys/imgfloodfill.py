#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy


if __name__ == "__main__":

    img = cv2.imread(sys.argv[1])
    cv2.imshow("image",img)

    h = img.shape[0]
    w = img.shape[1]
    mask = numpy.zeros((h+2,w+2), numpy.uint8)
    point = None

    def onMouse (event, x, y, flags, param):
        global point
        if flags & cv2.EVENT_FLAG_LBUTTON:
            print (x,y)
            point = x,y
            update()
            
    
    def update(dummy=None):
        mask[:] = 0 
        img2 = img.copy()
        cv2.floodFill(img2, mask, point, (255,255,255), (cv2.getTrackbarPos("low","image"), )*3, (cv2.getTrackbarPos("hi","image"), )*3,cv2.FLOODFILL_FIXED_RANGE)        
        cv2.circle(img2, point, 3, (0,0,255), -1)
        cv2.imshow("image",img2)
                
                



    cv2.createTrackbar('low', 'image', 20, 255, update)
    cv2.createTrackbar('hi', 'image', 20, 255, update)

    cv2.setMouseCallback("image",onMouse)

    cv2.waitKey(0)
