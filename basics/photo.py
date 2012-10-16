#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)
    i = 1
    j = 1
    cont = -1
    while True:

        f, img = camera.read()
        cv2.putText(img,"press f to take a photo and ESC for exit",(20,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),1)
        cv2.imshow("camera",img)
        cv2.cv.MoveWindow("camera",10,10)
        c = cv2.waitKey (5)

        #if you press f opens a new window with the image that is in the webcam at that moment,that is, does a photo
        if (c == 102):
            cont = cont+1
            if (cont%4 == 0):
                j = j+1
                i = 1
            
            cv2.imwrite("foto"+str(i)+".jpg",img,(cv2.cv.CV_IMWRITE_JPEG_QUALITY,88))
            imgShape = img.shape
            cv2.imshow("foto"+str(cont),cv2.resize(img,(int(imgShape[1]*0.5),int(imgShape[0]*0.5))))
            cv2.cv.MoveWindow("foto"+str(cont),400+100*j,10+100*i)
            i = i+1

        #if you press f, close all windows
        elif (c == 27):
            break
