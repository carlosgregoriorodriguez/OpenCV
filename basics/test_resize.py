#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    while True:

      f,img = camera.read()

      imgShape = img.shape

      cv2.imshow("webcam",img)
        
      cv2.imshow("webcam+resize1.5",cv2.resize(img,(int(imgShape[1]*1.5),int(imgShape[0]*1.5))))

      cv2.imshow("webcam+resize0.5",cv2.resize(img,(int(imgShape[1]*0.25),int(imgShape[0]*0.25))))
                 
      if (cv2.waitKey(5) != -1):
      	break
