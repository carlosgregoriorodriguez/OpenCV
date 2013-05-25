#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys

def onblur_x(pos):
    cv2.imshow("image", cv2.blur(img, (pos,cv2.getTrackbarPos("blur_y","image"))))

def onblur_y(pos):
    cv2.imshow("image",cv2.blur(img, (cv2.getTrackbarPos("blur_x","image"),pos)))

def onGaussBlur(pos):
    if (pos == 1):
         cv2.imshow("image",cv2.GaussianBlur(img,(3,3), 0))
    elif(pos == 2):
         cv2.imshow("image", cv2.GaussianBlur(img,(5,5), 0))
    elif(pos == 3):
         cv2.imshow("image",cv2.GaussianBlur(img,(7,7), 0))

def onMedianBlur(pos):
    if (pos%2 != 0):
        cv2.imshow("image_MB",cv2.medianBlur(img, pos))

def onBilFil_c(pos):
    cv2.imshow("image_BF",cv2.bilateralFilter(img,6 , pos, pos))


if __name__ == "__main__":

    img = cv2.imread(sys.argv[1])
    cv2.imshow("image",img)

    cv2.createTrackbar("blur_x","image",1,100,onblur_x)
    cv2.createTrackbar("blur_y","image",1,100,onblur_y)

    cv2.createTrackbar("GaussBlur","image",0,3,onGaussBlur)
    
    #When the value of the trackbar is 0,1,2 or a even number, the image stays as it was, isn't anything new
    cv2.createTrackbar("MedianBlur","image",2,13,onMedianBlur)
    
    cv2.createTrackbar("BilFilter_c","image",0,300,onBilFil_c)


    cv2.waitKey(0) 
