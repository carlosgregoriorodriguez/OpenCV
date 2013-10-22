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
    img1 = cv2.imread(img1_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    img2 = cv2.imread(img2_name, cv2.CV_LOAD_IMAGE_GRAYSCALE)
 
    #Difference
    diff = cv2.absdiff(img1,img2)
    cv2.imshow("diff",diff)

    #Dilate
    diff = cv2.dilate(diff, kernel=None, iterations=3)
    cv2.imshow("dilate",diff)

    #Threshold
    value, diff = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
    cv2.imshow("threshold",diff)

    #Contours 
    contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    
    cv2.drawContours(img1, contours, -1, color=255, thickness=3)
    cv2.drawContours(img2, contours, -1, color=0, thickness=3)
    cv2.imshow("img1",img1)
    cv2.imshow("img2",img2)
        
    cv2.waitKey(0)
