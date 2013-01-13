#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np

help_message = '''USAGE: butt_contour.py [<image>,<image>,...]

Keys:
  a    - shows all contours 
  s    - shows one by one the contours
               m  - shows the next contour
               n  - shows the previus contour
'''

if __name__ == "__main__":
    print help_message

    images_name = sys.argv[1:]
    template = cv2.imread('qp.jpg')
    
    for img_name in images_name :
        img = cv2.imread(img_name)#butterflies_resize
        imgfound = cv2.matchTemplate(img,template, cv2.TM_SQDIFF_NORMED)
        minV,maxV,minL,maxL = cv2.minMaxLoc(imgfound)
        point = (minL[0], minL[1]-35)

        reduced_img = np.zeros(img.shape,np.uint8)+255
        reduced_img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)]
        
        img_but = img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)]
        img_but = cv2.cvtColor(img_but, cv2.cv.CV_BGR2XYZ)
        img_but = cv2.medianBlur(img_but,3)
        img_erode = cv2.erode(img_but, kernel=None,iterations=3)    
        
        imgbn = cv2.cvtColor(img_erode,cv2.cv.CV_BGR2GRAY)
        canny = cv2.Canny(imgbn,144,67) 
        rawcontours,hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);
        cv2.drawContours(img_but, rawcontours, -1, (255,0,0), 1, cv2.CV_AA)
        reduced_img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = img_but
        mask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)
        mask[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = canny

        cv2.floodFill(reduced_img, mask, (point[0]+point[1]+int(2*point[1]/3)-20,10), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
        cv2.floodFill(reduced_img, mask, (point[0]+15,point[1]-38), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
        #cv2.circle(reduced_img,(point[0]+128,point[1]-3),3,(255,0,255))
        cv2.floodFill(reduced_img, mask, (point[0]+128,point[1]-6), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
        cv2.floodFill(reduced_img, mask, (point[0]+11,point[1]-6), (255, 255, 255), (2,)*3, (100,)*3)
        
        imgbn = cv2.cvtColor(reduced_img,cv2.cv.CV_BGR2GRAY)
        retVal,img_thres = cv2.threshold(imgbn,254,255,cv2.THRESH_BINARY)
        #cv2.imshow('img',img_thres)

        imgcanny = cv2.Canny(img_thres, 48, 22)
        contours, hierarchy = cv2.findContours(imgcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        i = 0
        
        cv2.imshow('img',img)
        img2 = img.copy()
        key = cv2.waitKey(0)
        if key == ord('a'):#muestra todos los contornos y para
            cv2.drawContours(img2, contours, -1, (255,0,155))
            cv2.imshow('img',img2)
        elif key == ord('s'):#muestra el contorno i
            i = 0
            while i < len(contours):
                img2 = img.copy()
                cv2.drawContours(img2, contours, i,(255,0,155))
                cv2.imshow('img',img2)
                k = cv2.waitKey(0)
                if k == ord('m'):
                    i = i+1
                elif k == ord('n'):
                    i = i-1
                else:
                    cv2.drawContours(img2, contours, -1, (255,0,155))
                    i = len(contours)
       

        cv2.waitKey(0)
