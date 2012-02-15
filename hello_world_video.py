#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
          
if __name__ == "__main__":

    camera =  cv2.VideoCapture(0)
    while True:
        f,img = camera.read()
        cv2.imshow("cam",img)
        if (cv2.waitKey (5) != -1):
            break
