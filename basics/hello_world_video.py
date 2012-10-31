#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
          
if __name__ == "__main__":

    if (len(sys.argv) > 1):
        target = sys.argv[1]
    else:
        target = 0
    
    camera =  cv2.VideoCapture(target)
    while True:
        f,img = camera.read()
        cv2.imshow("webcam",img)
        if (cv2.waitKey (5) != -1):
            break
