#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys

def ondx(pos):
    global img
    if pos == 0 and cv2.getTrackbarPos("dy","image") == 0 :
        cv2.imshow("image",i)
    else:
        cv2.imshow("image",cv2.Sobel(img,0,pos,cv2.getTrackbarPos("dy","image")))

def ondy(pos):
    global img
    if pos == 0 and cv2.getTrackbarPos("dx","image") == 0 :
        cv2.imshow("image",i)
    else:
        cv2.imshow("image",cv2.Sobel(img,0,cv2.getTrackbarPos("dx","image"),pos))

if __name__ == "__main__":


    i = cv2.imread(sys.argv[1])
    img = i.copy()

    cv2.imshow("image",img)

    cv2.createTrackbar("dx","image",0,2,ondx)
    cv2.createTrackbar("dy","image",0,2,ondy)

    cv2.waitKey(0) 
