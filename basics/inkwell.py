#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2;
import sys;
import numpy as np;

def onMouseBGR (event, x, y, flags, param):
    if flags & cv2.EVENT_FLAG_LBUTTON:
        print 'image_bgr (BGR)'
        update(img,x,y)
def onMouseLAB (event, x, y, flags, param):
    if flags & cv2.EVENT_FLAG_LBUTTON:
        print 'image_lab (LAB)'
        update(imglab,x,y)
def onMouseHSV (event, x, y, flags, param):
    if flags & cv2.EVENT_FLAG_LBUTTON:
        print 'image_hsv (HSV)'
        update(imghsv,x,y)
def onMouseXYZ (event, x, y, flags, param):
    if flags & cv2.EVENT_FLAG_LBUTTON:
        print 'image_xyz (XYZ)'
        update(imgxyz,x,y)
def onMouseYCrCb (event, x, y, flags, param):
    if flags & cv2.EVENT_FLAG_LBUTTON:
        print 'image_YCrCb (YCrCb)'
        update(imgYCrCb,x,y)
def onMouseLUV (event, x, y, flags, param):
    if flags & cv2.EVENT_FLAG_LBUTTON:
        print 'image_luv (LUV)'
        update(imgluv,x,y)

def update(image,x,y):    
    m1 = 0
    m2 = 0
    m3 = 0
    k = 0
    for i in range(-2,3):
        for j in range(-2,3):
           # a = cv2.split(image)[0]
           # b = cv2.split(image)[1]
           # c = cv2.split(image)[2]
            #print k
            k = k+1
           # image[y+j,x+i,0]= 0
           # image[y+j,x+i,1]= 129
           # image[y+j,x+i,2] = 0
            m1 = m1 + image[y+j,x+i,0]
            m2 = m2 + image[y+j,x+i,1]
            m3 = m3 + image[y+j,x+i,2]
    
    m1 = m1/25.0
    m2 = m2/25.0
    m3 = m3/25.0
    suma = (m1 + m2 + m3)/100
    print "valor absoluto", '('+str(m1)+', '+str(m2)+', '+str(m3)+')'
    print "porcentaje absoluto", '('+"{0:.2f}".format(m1/2.55)+'%, '+"{0:.2f}".format(m2/2.55)+'%, '+"{0:.2f}".format(m3/2.55)+'%)'
    print "porcentaje relativo", '('+"{0:.2f}".format(m1/suma)+'%, '+"{0:.2f}".format(m2/suma)+'%, '+"{0:.2f}".format(m3/suma)+'%)'
    cv2.imshow('img',image)

if __name__ == "__main__":

    if (len(sys.argv)== 1):
        img = cv2.imread('colorcheck.jpg')
    else: img = cv2.imread(sys.argv[1])


    img2 = img.copy()
   # img2.astype(float)
    #img2 = img2*(1/255)
    imglab = cv2.cvtColor(img2, cv2.cv.CV_BGR2Lab)
   # imghsv = cv2.cvtColor(img,cv2.cv.CV_BGR2HSV)
   # imgxyz = cv2.cvtColor(img, cv2.cv.CV_BGR2XYZ)
   # imgYCrCb = cv2.cvtColor(img,cv2.cv.CV_BGR2YCrCb)
   # imgluv = cv2.cvtColor(img2,cv2.cv.CV_BGR2Luv)
    cv2.imshow('image_bgr',img)
    cv2.imshow('image_lab', imglab)
   # cv2.imshow('image_hsv',imghsv)
   # cv2.imshow('image_xyz',imgxyz)
   # cv2.imshow('image_YCrCb',imgYCrCb)
   # cv2.imshow('image_luv',imgluv)

   # L = cv2.split(imglab)[0]
   # a = cv2.split(imglab)[1]
   # b = cv2.split(imglab)[2]

   # cv2.imshow('L',cv2.merge(a,b))
   # cv2.imshow('a', a)
   # cv2.imshow('b',b)

    cv2.setMouseCallback('image_bgr',onMouseBGR)
    cv2.setMouseCallback('image_lab',onMouseLAB)
    cv2.setMouseCallback('image_hsv',onMouseHSV)
    cv2.setMouseCallback('image_xyz',onMouseXYZ)
    cv2.setMouseCallback('image_YCrCb',onMouseYCrCb)
    cv2.setMouseCallback('image_luv',onMouseLUV)


    cv2.waitKey(0)
