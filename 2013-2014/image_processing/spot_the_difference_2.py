#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3

import cv2
import sys

if __name__ == "__main__":
    if (len(sys.argv) >= 3):
        img1_name = sys.argv[1]
        img2_name = sys.argv[2]
    else:
        img1_name = "../img/beach1.jpg"
        img2_name = "../img/beach2.jpg"

    #Load images
    img1 = cv2.imread(img1_name)
    img2 = cv2.imread(img2_name)

    #Convert to grayscale
    img1_bn = cv2.cvtColor(img1,cv2.cv.CV_BGR2GRAY)
    img2_bn = cv2.cvtColor(img2,cv2.cv.CV_BGR2GRAY)
 
    #Difference
    diff = cv2.absdiff(img1_bn,img2_bn)
    cv2.imshow("diff",diff)

    #Dilate
    diff = cv2.dilate(diff, kernel=None, iterations=5)
    cv2.imshow("dilate",diff)

    #Threshold
    value, diff = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    cv2.imshow("threshold",diff)

    #Contours 
    contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #differences with cv2.CHAIN_APPROX_SIMPLE

    #Nicer visualisation
    for c in contours:
        if len(c) > 5: #fitEllipse requierement
            cv2.ellipse(img1, cv2.fitEllipse(c), color=(0,0,255))
            cv2.ellipse(img2, cv2.fitEllipse(c), color=(0,255,0))
        
    cv2.imshow("img1",img1)
    cv2.imshow("img2",img2)
    cv2.waitKey(0)
