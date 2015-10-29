#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
          
def filter_color(img):
    img = cv2.inRange(img,lowerb=(40,40,120),upperb=(65,65,165))
    #img = cv2.inRange(img,lowerb=(120,100,60),upperb=(160,140,100))
    img  = cv2.dilate(img,kernel=None,iterations=5) 
    return img

if __name__ == "__main__":

    if (len(sys.argv) > 1):
        if (sys.argv[1] == "0"):
		name = 0
        else:
            name = sys.argv[1]
	
    else:
        name = "data/treme.avi"
    
    name = 1
    camera =  cv2.VideoCapture(name)
    f, img = camera.read()		
    while f:	
        #img = img[:,:,0] 
	cv2.imshow("video", img)
        filtered = filter_color(img)
        cv2.imshow("processed", filtered)
        f, img = camera.read()		
        if (cv2.waitKey (5) != -1):
            break
