#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np

help_message = '''USAGE: butt_contour.py [<image>,<image>,...]

Keys:
  a    - shows all the final contours in img_final
'''

def dummy(pos):
    print pos

def onMouse(event, x, y, flag, param):
    global seed_pt
    if flag & cv2.EVENT_FLAG_LBUTTON:
        seed_pt = x, y
        update()

def update():
    global img, img_but, reduced_img, seed_pt, connectivity
    img2 = img.copy()
    img_but2 = img_but.copy()
    reduced_img2 = reduced_img.copy()

    mb = cv2.getTrackbarPos('medianBlur','config')
    if (mb%2 != 0):
        img_but2 = cv2.medianBlur(img_but2,mb)
    else:
        img_but2 = cv2.medianBlur(img_but2,mb-1)
    cv2.imshow('median_blur',img_but2)

    it = cv2.getTrackbarPos('erode_it','config')
    img_erode = cv2.erode(img_but2, kernel=None, iterations = 3)
    cv2.imshow('erode',img_erode)
    
    imgbn = cv2.cvtColor(img_erode,cv2.cv.CV_BGR2GRAY)
    canny = cv2.Canny(imgbn,cv2.getTrackbarPos('canny_hi(1)','config'),cv2.getTrackbarPos('canny_lo(1)','config'))
    cv2.imshow('canny(1)',canny)
    rawcontours,hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);
    cv2.drawContours(img_but2, rawcontours, -1, (255,0,0), 1, cv2.CV_AA)
    reduced_img2[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = img_but2
    mask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)
    mask[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = canny
        
    if seed_pt ==  None:
        seed_pt = (point[0]+point[1]+int(2*point[1]/3)-20,10) 
    flags = connectivity
    if fixed_range:
        flags |= cv2.FLOODFILL_FIXED_RANGE    
    cv2.floodFill(reduced_img2, mask, seed_pt, (255, 255, 255), (cv2.getTrackbarPos('floodfill_lo','config'),)*3, (cv2.getTrackbarPos('floodfill_hi','config'),)*3, flags)
    
    cv2.imshow('floodfill',reduced_img2)    
    imgbn = cv2.cvtColor(reduced_img2,cv2.cv.CV_BGR2GRAY)
    retVal,img_thres = cv2.threshold(imgbn,cv2.getTrackbarPos('threshold','config'),255,cv2.THRESH_BINARY)
    cv2.imshow('thres',img_thres)
    
    imgcanny = cv2.Canny(img_thres,cv2.getTrackbarPos('canny_hi(2)','config'),cv2.getTrackbarPos('canny_lo(2)','config'))
    cv2.imshow('canny(2)',imgcanny)
    contours, hierarchy = cv2.findContours(imgcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    return contours


if __name__ == "__main__":
    print help_message

    images_name = sys.argv[1:]
    template = cv2.imread('qp.jpg')


    cv2.namedWindow('config')
    cv2.namedWindow('floodfill')
    cv2.createTrackbar('floodfill_hi','config',60,255,dummy)
    cv2.createTrackbar('floodfill_lo','config',2,255,dummy)
    cv2.createTrackbar('canny_hi(1)','config',144,600,dummy)
    cv2.createTrackbar('canny_lo(1)','config',67,600,dummy)
    cv2.createTrackbar('canny_hi(2)','config',48,600,dummy)
    cv2.createTrackbar('canny_lo(2)','config',22,600,dummy)
    #cv2.createTrackbar('erode_it','config',3,15,dummy)
    cv2.createTrackbar('medianBlur','config',3,15,dummy)
    cv2.createTrackbar('threshold','config',254,255,dummy)

    cv2.setMouseCallback('floodfill',onMouse)


    for img_name in images_name :
       
        connectivity = 4
        fixed_range = False
        seed_pt = None

        img = cv2.imread(img_name)#butterflies_resize
        imgfound = cv2.matchTemplate(img,template, cv2.TM_SQDIFF_NORMED)
        minV,maxV,minL,maxL = cv2.minMaxLoc(imgfound)
        point = (minL[0], minL[1]-35)
        
        reduced_img = np.zeros(img.shape,np.uint8)+255
        reduced_img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)]
        
        img_but = img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)]
        #img_but = cv2.cvtColor(img_but, cv2.cv.CV_BGR2XYZ)
    
        contours = update()
        



        while True:
            img3 = img.copy()
            cv2.imshow('img',img3)
            key = cv2.waitKey(5)
            if key == ord('a'):#muestra todos los contornos 
                cv2.drawContours(img3, contours, -1, (255,0,155))
                cv2.imshow('img_final',img3)
            if key == ord('f'):
                fixed_range = not fixed_range
            if key == ord('c'):
                connectivity = 12-connectivity
            if key == 27:
                break
            contours = update()
