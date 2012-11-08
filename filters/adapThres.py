#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys

def onThreshold (pos):
    size = cv2.getTrackbarPos("blockSize","image")
    if size%2 == 0:
        size = size+1

    if pos == 0:
        img2 = cv2.adaptiveThreshold(img,cv2.getTrackbarPos("maxValue","image"),cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,size,cv2.getTrackbarPos("cte","image"))
    else: img2 = cv2.adaptiveThreshold(img,cv2.getTrackbarPos("maxValue","image"),cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,size,cv2.getTrackbarPos("cte","image"))
    cv2.imshow("image",img2)

def onMaxValue (pos):
    size = cv2.getTrackbarPos("blockSize","image")
    if size%2 == 0:
        size = size+1

    thres = cv2.getTrackbarPos("threshold","image")
    if thres == 0:
        img2 = cv2.adaptiveThreshold(img,pos,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,size,cv2.getTrackbarPos("cte","image"))
    else: img2 = cv2.adaptiveThreshold(img,pos,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,size,cv2.getTrackbarPos("cte","image"))
    cv2.imshow("image",img2)

def onBlockSize (pos):
   if (pos%2 != 0):
       thres = cv2.getTrackbarPos("threshold","image")
       if thres == 0:
           img2 = cv2.adaptiveThreshold(img,cv2.getTrackbarPos("maxValue","image"),cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,pos,cv2.getTrackbarPos("cte","image"))
       else:  img2 = cv2.adaptiveThreshold(img,cv2.getTrackbarPos("maxValue","image"),cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,pos,cv2.getTrackbarPos("cte","image"))
       cv2.imshow("image",img2)

def onCte (pos):
    size = cv2.getTrackbarPos("blockSize","image")
    if size%2 == 0:
        size = size+1

    thres = cv2.getTrackbarPos("threshold","image")
    if thres == 0:
        img2 = cv2.adaptiveThreshold(img,cv2.getTrackbarPos("maxValue","image"),cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,size,pos)
    else:  img2 = cv2.adaptiveThreshold(img,cv2.getTrackbarPos("maxValue","image"),cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,size,pos)
    cv2.imshow("image",img2)

if __name__ == "__main__":

    img = cv2.imread(sys.argv[1])

    img = cv2.cvtColor(img,cv2.cv.CV_RGB2GRAY)

    img2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,3,0)
    cv2.imshow("image",img2)
    cv2.imshow("img",img)

    cv2.createTrackbar("threshold","image",0,1,onThreshold)
    cv2.createTrackbar("maxValue","image",255,255,onMaxValue)
    cv2.createTrackbar("blockSize","image",3,600,onBlockSize)
    cv2.createTrackbar("cte","image",0,100,onCte)


    cv2.waitKey(0) 
