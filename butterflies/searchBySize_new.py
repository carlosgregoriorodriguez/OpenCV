#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np
import calcBinaryImage

help_message = '''USAGE: searchBySize_new.py [<image for compare>,<image>,...]

Keys:

 STEP 1
  g    -   save the binary image for later comparison
  k    -   reset the values chosen for the image
  ESC  -   moves to the next image for analyzing

'''  
def dummy(pos):
    a = pos

def compare():
    global j

    eps = [cv2.getTrackbarPos('eps1___*e-3','config2')*10**(-3),cv2.getTrackbarPos('eps2___*e-4','config2')*10**(-4),cv2.getTrackbarPos('eps3___*e-4','config2')*10**(-4),cv2.getTrackbarPos('eps4___*e-5','config2')*10**(-5),cv2.getTrackbarPos('eps5___*e-9','config2')*10**(-9),cv2.getTrackbarPos('eps6___*e-7','config2')*10**(-7),cv2.getTrackbarPos('eps7___*e-8','config2')*10**(-8)]
        
    imshow = []
    for im in compare_images:
        img = im[0]
        moments1 = cv2.moments(img,True)
        H1 = cv2.HuMoments(moments1) 
        cv2.putText(im[1],str(H1[0:2]),(50,img.shape[0]-100),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))
        cv2.putText(im[1],str(H1[2:4]),(50,img.shape[0]-75),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))
        cv2.putText(im[1],str(H1[4:6]),(50,img.shape[0]-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))
        cv2.putText(im[1],str(H1[6:8]),(50,img.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))          
        for i in range(len(H)):
            if H[i]> H1[i]+eps[i] or H[i]<H1[i]-eps[i]:
                break  
            elif i == len(H)-1:
                imshow = imshow+[im[1]]
        j = 1
        for im in imshow:
            cv2.imshow('im_'+str(j),im)
            j = j+1



if __name__ == "__main__":
    print help_message

    images_name = sys.argv[1:]
    template = cv2.imread('qp.jpg')
    compare_images = []



#########   STEP 1   ###########################

    for img_name in images_name :
        img = cv2.imread(img_name)
        compare_images = compare_images + [calcBinaryImage.calcMask(img)]


################  STEP2   #####################################

    cv2.destroyAllWindows()

    print '''

 STEP 2 (comparison)
  s    -   look for the more similar images with the chosen data
  q    -   EXIT

'''


    cv2.namedWindow('config2')
    cv2.createTrackbar('eps1___*e-3','config2',10,100,dummy)
    cv2.createTrackbar('eps2___*e-4','config2',50,100,dummy)
    cv2.createTrackbar('eps3___*e-4','config2',80,100,dummy)
    cv2.createTrackbar('eps4___*e-5','config2',80,100,dummy)
    cv2.createTrackbar('eps5___*e-9','config2',1000,1000,dummy)
    cv2.createTrackbar('eps6___*e-7','config2',1000,1000,dummy)
    cv2.createTrackbar('eps7___*e-8','config2',10,100,dummy)

    pimg = compare_images[0][0]
    img = compare_images[0][1].copy()
    moments = cv2.moments(pimg,True)
    H = cv2.HuMoments(moments)
    cv2.putText(img,str(H[0:2]),(50,img.shape[0]-100),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))
    cv2.putText(img,str(H[2:4]),(50,img.shape[0]-75),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))
    cv2.putText(img,str(H[4:6]),(50,img.shape[0]-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))
    cv2.putText(img,str(H[6:8]),(50,img.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))
    compare()

    while True:
        cv2.imshow('image',img)
        key = cv2.waitKey(5)
        if key == ord('s'):
            for k in range(j):
                cv2.destroyWindow('im_'+str(k))
            cv2.imshow('image',img)
            compare()
        if key == ord('q'):
            break
    
        
        
