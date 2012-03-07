#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)
     
    f,img = camera.read()   
    imgShape = img.shape
    h = imgShape[0]
    l = imgShape[1]
    print imgShape
    print "h "+str(h)
    print "l "+str(l)
    while True:

        f,img = camera.read()

        cv2.imshow("webcam",img)        

        cv2.imshow("trozo1", cv2.getRectSubPix(img,(l/2,h),(l/4,h/2)))
        cv2.imshow("trozo2", cv2.getRectSubPix(img,(l/2,h),(3*l/4,h/2)))

        if (cv2.waitKey(5) != -1):    
            break
