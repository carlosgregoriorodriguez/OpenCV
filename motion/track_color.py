#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np          

def joinImages (images):
	w = images[0][0].shape[1];
	h = images[0][0].shape[0];
	img = np.zeros((len(images)*h, len(images[0])*w,3), np.uint8);
	for i in range(len(images)):
		for j in range(len(images[0])):
			if (images[i][j] != None):  
				if(len(images[i][j].shape) == 3):
					img[i*h:(i+1)*h,j*w:(j+1)*w] = images[i][j];
				else:
					for k in range(3):
						img[i*h:(i+1)*h,j*w:(j+1)*w,k] = images[i][j];
					
	return img;
          
          
def filter_color(img):
    img = cv2.inRange(img,lowerb=(40,40,120),upperb=(65,65,165))
    #img = cv2.inRange(img,lowerb=(120,100,60),upperb=(160,140,100))
    img  = cv2.dilate(img,kernel=None,iterations=5) 
    return img

def filter_high(img, value):
    img = cv2.inRange(img,lowerb=value,upperb=255)
    return img
if __name__ == "__main__":

    if (len(sys.argv) > 1):
        if (sys.argv[1] == "0"):
		name = 0
        else:
            name = sys.argv[1]
	
    else:
        name = "data/treme.avi"
    
    camera =  cv2.VideoCapture(name)
    f, img = camera.read()		
    while f:	
        #img = img[:,:,0] 
        imgB, imgG, imgR = cv2.split(img) 
        cv2.cvtColor(img, cv2.COLOR_RGB2HSV);
        imgHSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        imgH, imgS, imgV = cv2.split(imgHSV) 
        filteredS = filter_high(imgS,170)
        filteredV = filter_high(imgV,100)
        filteredG = filter_high(imgG,70)
        filteredR = filter_high(imgR,70)
        filteredB = filter_high(imgB,100)
        sANDv = cv2.bitwise_and(filteredS,filteredV)
        gsv = cv2.bitwise_and(sANDv,filteredG)
        rsv = cv2.bitwise_and(sANDv,filteredR)
        bsv = cv2.bitwise_and(sANDv,filteredB)
        res = joinImages([[imgR,imgG,imgB],[gsv, rsv, bsv]])
        cv2.imshow("",res)
        f, img = camera.read()		
        if (cv2.waitKey (5) != -1):
            break
