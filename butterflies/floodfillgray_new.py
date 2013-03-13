#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np

help_message = '''USAGE: floodfillgray_new.py [<image>,<image>,...]

Keys:
  m    - flooded next image
  n    - flooded previus image
'''

def flood_eps(pos):
    img = flooded(cv2.imread(name_images[l]),pos,cv2.getTrackbarPos('hi','image'),cv2.getTrackbarPos('lo','image'))
    cv2.imshow('image',img)

def flood_hi(pos):
    img = flooded(cv2.imread(name_images[l]),cv2.getTrackbarPos('epsilon','image'),pos,cv2.getTrackbarPos('lo','image'))
    cv2.imshow('image',img)

def flood_lo(pos):
    img = flooded(cv2.imread(name_images[l]),cv2.getTrackbarPos('epsilon','image'),cv2.getTrackbarPos('hi','image'),pos)
    cv2.imshow('image',img)

def flooded(img, epsilon, hi, lo):
    img2 = np.array(img,float)
    img2 = img2/3
    img3 = img2[:,:,0]+img2[:,:,1]+img2[:,:,2]
    m1 = np.ma.masked_less(img3,hi)
    m2 = np.ma.masked_greater(img3,lo)
    m1 = 1-m1.mask
    m2 = 1-m2.mask
    m3 = np.ma.mask_or(m1,m2)
    m3 = 1-m3
    m3 = 1-m3
    w, h = img.shape[:2]
    aa = np.zeros((w,h),float)

    b = cv2.split(img)[0]
    g = cv2.split(img)[1]
    r = cv2.split(img)[2]

    b = np.array(b,np.int16)
    g = np.array(g,np.int16)
    r = np.array(r,np.int16)

    cmax = (b+g+abs(b-g))/2
    ma = (cmax+r+abs(cmax-r))/2
    cmin = (b+g-abs(b-g))/2
    mi = (cmin+r-abs(cmin-r))/2
    a = ma - mi

    m = np.ma.masked_less(a,epsilon)
    m = 1 - m.mask
    
    M = np.ma.mask_or(m,m3)
    M = 1-M
    mas = np.zeros((M.shape[0],M.shape[1],3),np.uint8)
    mas[:,:,0]=M
    mas[:,:,1]=M
    mas[:,:,2]=M
    i = np.ma.array(img,mask=mas)
    i.set_fill_value(255)
    img = i.filled()
    
    return img


if __name__ == '__main__':
    print help_message
    global l

    name_images = sys.argv[1:]
    l = 0

    cv2.namedWindow('image')
    cv2.createTrackbar('epsilon','image',10,255,flood_eps)
    cv2.createTrackbar('hi','image',200,255,flood_hi)
    cv2.createTrackbar('lo','image',20,255,flood_lo)

    img = flooded(cv2.imread(name_images[l]),cv2.getTrackbarPos('epsilon','image'),cv2.getTrackbarPos('hi','image'),cv2.getTrackbarPos('lo','image'))
    cv2.imshow('image',img)

    while True:
        k = cv2.waitKey(5)
        if k == ord('m'):
            if l < len(name_images)-1:
                l = l+1
                img = flooded(cv2.imread(name_images[l]),cv2.getTrackbarPos('epsilon','image'),cv2.getTrackbarPos('hi','image'),cv2.getTrackbarPos('lo','image'))
                cv2.imshow('image',img)
            else:
                break
        if k == ord('n'):
            if l>0:
                l = l-1
                img = flooded(cv2.imread(name_images[l]),cv2.getTrackbarPos('epsilon','image'),cv2.getTrackbarPos('hi','image'),cv2.getTrackbarPos('lo','image'))
                cv2.imshow('image',img)
        if k == 27:
            break
        
