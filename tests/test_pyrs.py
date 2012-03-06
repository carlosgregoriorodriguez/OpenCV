#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

#pyrUp and PyrDown

import  cv2


if __name__ == "__main__":

 camera = cv2.VideoCapture(0)

 while True:
     
     f,img = camera.read()

     cv2.imshow("webcam",img)

     cv2.imshow("webcam+pyrDown",cv2.pyrDown(img))

     cv2.imshow("webcam+pyrUp",cv2.pyrUp(img))

     cv2.imshow("webcam+pyrUp(pyrDown)",cv2.pyrUp(cv2.pyrDown(img)))

     cv2.imshow("webcam+pyrDown(pyrUp)",cv2.pyrDown(cv2.pyrUp(img)))

     
     if (cv2.waitKey(1) != -1):
         break
            
