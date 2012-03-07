#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2


if __name__ == "__main__":


  camera = cv2.VideoCapture(0)

  g,im = camera.read()

  while True:

    f,img = camera.read()

    #Python: cv2.copyMakeBorder(src, top, bottom, left, right, borderType[, dst[, value]]) → dst¶

    cv2.imshow("BORDER_DEFAULT",cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_DEFAULT))
      
    #cv2.imshow("BORDER_TRANSPARENT",cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_TRANSPARENT))
 
    #cv2.imshow("BORDER_ISOLATED",cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_ISOLATED))
  
    cv2.imshow("BORDER_CONSTANT",cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_CONSTANT))

    cv2.imshow("BORDER_WRAP",cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_WRAP))

    cv2.imshow("BORDER_REFLECT_101",cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_REFLECT_101))

    if(cv2.waitKey(5)!=-1):
      break




