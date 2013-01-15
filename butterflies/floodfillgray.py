#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np

help_message = '''USAGE: floodfillgray.py [<image>,<image>,...]

Keys:
  f    - flooded
  m    - flooded next image
  n    - flooded previus image
'''
def update(pos):
        print '',

def flooded():
    global l, name_images
   # print  '                '+str(l)
    img = cv2.imread(name_images[l])
    lo = cv2.getTrackbarPos('lo','image')
    hi = cv2.getTrackbarPos('hi','image')
    epsilon = cv2.getTrackbarPos('epsilon','image')
    w, h = img.shape[:2]
    for i in range(w):
        for j in range(h):
            b = img[i,j,0]
            g = img[i,j,1]
            r = img[i,j,2]
            '''
            pb = img[i,j,0]*100/255
            pg = img[i,j,1]*100/255
            pr = img[i,j,2]*100/255
            '''
            ma = max(b,g,r)
            mi = min(b,g,r)
            med = b/3+g/3+r/3
            if ma-mi<epsilon and med<hi and med>lo:# o ma<hi and mi>lo
                img[i,j,0] = 255
                img[i,j,1] = 255
                img[i,j,2] = 255
    cv2.imshow('image',img)


if __name__ == '__main__':
    print help_message

    name_images = sys.argv[1:]
    l = 0

    cv2.namedWindow('image')
    cv2.createTrackbar('epsilon','image',10,255,update)
    cv2.createTrackbar('hi','image',200,255,update)
    cv2.createTrackbar('lo','image',20,255,update)
    flooded()
    
    while True:
        k = cv2.waitKey(5)
        if k == ord('f'):
            flooded()
        if k == ord('m'):
            if l < len(name_images)-1:
                l = l+1
                flooded()
            else:
                break
        if k == ord('n'):
            if l>0:
                l = l-1
                flooded()
        if k == 27:
            break
        
