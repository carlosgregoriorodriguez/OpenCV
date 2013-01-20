#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import numpy as np
import sys

def help():
   print ">"*40
   print "Usage: python polares.py [filename]"
   print "click left button: polares with that central point"
   print "q to quit"
   print "<"*40

img = None

def onmouse(event, x, y, flags, param):
   if flags & cv2.EVENT_FLAG_LBUTTON:
      polar(img,(x,y))

def polar(img,center):
   cv2.circle(img, center, 5, (0,0,255),-1)
   oldimg = cv2.cv.fromarray(img)
   newimg = cv2.cv.fromarray(np.copy(img))
   cv2.cv.LogPolar(oldimg,newimg,center,100)
   cv2.cv.ShowImage("polar",newimg)
   cv2.imshow('img', img)

if __name__ == "__main__":
    help()
    video = False;
    filename = '../img/stop.jpg';
    cam = False;
    global img
    if (len(sys.argv)>1):
       filename = sys.argv[1];
    firstimage = False
    while True:		
       if not firstimage:
          img = cv2.imread(filename);
          cv2.imshow('img', img)
          cv2.setMouseCallback('img', onmouse)
          firstimage = True

       key = cv2.waitKey(5);
       if (key != -1):
          if key & 255 == 113 : #tecla q
             break
