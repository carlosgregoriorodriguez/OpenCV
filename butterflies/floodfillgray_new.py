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

def flooded(pos = None):
    global l, name_images

    img = cv2.imread(name_images[l])
    lo = cv2.getTrackbarPos('lo','image')
    hi = cv2.getTrackbarPos('hi','image')
    epsilon = cv2.getTrackbarPos('epsilon','image')
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
    


    '''
    for i in range(w):
        for j in range(h):
            b = img[i,j,0]
            g = img[i,j,1]
            r = img[i,j,2]
            aa[i,j] = np.max([b,g,r])-np.min([b,g,r])

    print aa
    '''




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
    
    cv2.imshow('image',img)


if __name__ == '__main__':
    print help_message

    name_images = sys.argv[1:]
    l = 0

    cv2.namedWindow('image')
    cv2.createTrackbar('epsilon','image',10,255,flooded)
    cv2.createTrackbar('hi','image',200,255,flooded)
    cv2.createTrackbar('lo','image',20,255,flooded)
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
        
