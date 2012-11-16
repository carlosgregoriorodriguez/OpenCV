#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys

if __name__ == "__main__":

    img = cv2.imread(sys.argv[1])
    cv2.imshow("image",img)

    h = img.shape[0]
    w = img.shape[1]
    angle = 0
    s = 90

    while True:
        c = cv2.waitKey(0)
    #if press r rotate
        if (c == 114):
            angle = angle + s 
            M = cv2.getRotationMatrix2D((w/2,h/2), angle, 1)
            img2 = cv2.warpAffine(img,M,(w,h))
            cv2.imshow("rotation",img2)
    #if press l modified de rotation angle (angle-angle/3)
        elif (c == 108):
                s = s-s/3
    #if press ESC close all windows
        elif (c == 27):
            break
        
