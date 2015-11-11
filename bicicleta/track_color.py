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

gl_S = 170
gl_V = 100
gl_R = 80
gl_G= 80
gl_B = 20
def onTrackbarSlideS(pos):
        global gl_S
        gl_S = pos
def onTrackbarSlideV(pos):
        global gl_V
        gl_V = pos
def onTrackbarSlideR(pos):
        global gl_R
        gl_R = pos
def onTrackbarSlideG(pos):
        global gl_G
        gl_G = pos
def onTrackbarSlideB(pos):
        global gl_B
        gl_B = pos
        
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
    cv2.namedWindow("video")
    cv2.createTrackbar("S","video",gl_S,255,onTrackbarSlideS)
    cv2.createTrackbar("V","video",gl_V,255,onTrackbarSlideV)
    cv2.createTrackbar("R","video",gl_R,255,onTrackbarSlideR)
    cv2.createTrackbar("G","video",gl_G,255,onTrackbarSlideG)
    cv2.createTrackbar("B","video",gl_B,255,onTrackbarSlideB)

    
    count = 0;
    f, img = camera.read()		
    while True:	
        if not f:
                camera =  cv2.VideoCapture(name)
                f, img = camera.read()
        if count == 0:
                #img = img[:,:,0] 
                imgB, imgG, imgR = cv2.split(img) 
                cv2.cvtColor(img, cv2.COLOR_RGB2HSV);
                imgHSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                imgH, imgS, imgV = cv2.split(imgHSV) 
                filteredS = filter_high(imgS,gl_S)
                filteredV = filter_high(imgV,gl_V)
                filteredG = filter_high(imgG,gl_R)
                filteredR = filter_high(imgR,gl_G)
                filteredB = filter_high(imgB,gl_B)
                res = cv2.bitwise_and(filteredS,filteredV)
                res = cv2.bitwise_and(res,filteredG)
                res = cv2.bitwise_and(res,filteredR)
                res = cv2.bitwise_and(res,filteredB)
                #res = joinImages([[imgR,imgG,imgB],[gsv, rsv, bsv]]
                cv2.imshow("ori",img)
                cv2.imshow("video",res)
        f, img = camera.read()
        count = (count + 1) % 6
        if (cv2.waitKey (1) != -1):
            break
