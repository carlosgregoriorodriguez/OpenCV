#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np

help_message = '''USAGE: calcBinaryImage.py [<image>,<image>,...]

Keys:

  g    -   save the binary image 
  k    -   reset the values chosen for the image
  ESC  -   moves to the next image for analyzing

'''

def onMouse(event, x, y, flag, param):
    global seed_pt
    if flag & cv2.EVENT_FLAG_LBUTTON:
        seed_pt = x, y
        on_flooding_trackbar()



def flooding(img):
    global reduced_img, new_flood
    if new_flood:
        img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = img_contours
        new_flood = False
        cv2.floodFill(img, mask, (point[0]+128,point[1]-6), (255, 255, 255), (3,)*3, (60,)*3, flags=4)
        cv2.floodFill(img, mask, (point[0]+11,point[1]-6), (255, 255, 255), (2,)*3, (100,)*3)
        cv2.floodFill(img, mask, (point[0]+point[1]+int(2*point[1]/3)-20,10), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
        cv2.floodFill(img, mask, (point[0]+15,point[1]-38), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
    flags = connectivity
    if fixed_range:
        flags |= cv2.FLOODFILL_FIXED_RANGE
    if seed_pt != None:
        lo = cv2.getTrackbarPos('floodfill_lo','config')
        hi = cv2.getTrackbarPos('floodfill_hi','config')
        cv2.floodFill(img, None, seed_pt, (255, 255, 255), (lo,)*3, (hi,)*3)
    cv2.imshow('floodfill',img)
    reduced_img = img.copy()
    return img



def filtering(img_butt):
    global img_filter
    mb = cv2.getTrackbarPos('medianBlur','config')
    if (mb%2 != 0):
        img = cv2.medianBlur(img_butt,mb)
    else:
        img = cv2.medianBlur(img_butt,mb-1)
    if cv2.getTrackbarPos('debug','config') >= 5:
        cv2.imshow('median_blur',img)
    img_filter = cv2.erode(img, kernel=None, iterations = 3)
    if cv2.getTrackbarPos('debug','config') >= 3:
        cv2.imshow('erode',img_filter)
    return img_filter



def calcContours(img):
    global mask
    imgbn = cv2.cvtColor(img,cv2.cv.CV_BGR2GRAY)
    canny = cv2.Canny(imgbn,cv2.getTrackbarPos('canny_hi','config'),cv2.getTrackbarPos('canny_lo','config'))
    if cv2.getTrackbarPos('debug','config') >= 4:
        cv2.imshow('canny',canny)
    mask = np.zeros((mask.shape[0], mask.shape[1]), np.uint8)
    mask[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = canny
    rawcontours,hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);
    imred = img_butt.copy()
    cv2.drawContours(imred, rawcontours, -1, (255,0,0), 1, cv2.CV_AA)
    return imred



def thresh(img):
    global final_mask
    imgbn = cv2.cvtColor(img,cv2.cv.CV_BGR2GRAY)
    retVal,img_thres = cv2.threshold(imgbn,254,255,cv2.THRESH_BINARY_INV)
    if cv2.getTrackbarPos('debug','config') >= 1:
        cv2.imshow('final_img', img_thres)
    final_mask = img_thres.copy()
    return img_thres



def prepare_image(pos = None):
    global reduced_img, img_contours
    img_filter = filtering(img_butt)
    img_contours = calcContours(img_filter)
    reduced_img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = img_contours
    img_flood = flooding(reduced_img)#modifica reduced_img
    cv2.imshow('floodfill',img_flood)
    img_thres = thresh(img_flood)    
    return img_thres



def on_filter_trackbar(pos=None):
    global new_flood
    cv2.destroyWindow('median_blur')
    cv2.destroyWindow('final_img')
    cv2.destroyWindow('erode')
    cv2.destroyWindow('img')
    cv2.destroyWindow('canny')
    new_flood = True
    prepare_image()



def on_contour_trackbar(pos=None):
    global img_contours, new_flood
    new_flood = True
    img_contours = calcContours(img_filter)
    img_flood = flooding(reduced_img)
    thresh(img_flood)



def on_flooding_trackbar(pos=None):
    img_flood = flooding(reduced_img)
    thresh(reduced_img)



def calcMask(img):
    global compare_images, new_flood, img_contours, seed_pt, reduced_img, img_butt, mask, point, connectivity, fixed_range, final_mask

    template = cv2.imread('qp.jpg')
    connectivity = 4
    seed_pt = None
    fixed_range = True
    img_filter = img
    img_contours = img
    mask = []
    mask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)

    imgfound = cv2.matchTemplate(img,template, cv2.TM_SQDIFF_NORMED)
    minV,maxV,minL,maxL = cv2.minMaxLoc(imgfound)
    point = (minL[0], minL[1]-35)
    
    reduced_img = np.zeros(img.shape,np.uint8)+255
    reduced_img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)]        
    
    img_butt = img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)]

    cv2.namedWindow('config')
    cv2.namedWindow('floodfill')
    cv2.createTrackbar('debug','config',0,5,on_filter_trackbar)
    cv2.createTrackbar('floodfill_hi','config',60,255,on_flooding_trackbar)
    cv2.createTrackbar('floodfill_lo','config',10,255,on_flooding_trackbar)
    cv2.createTrackbar('canny_hi','config',144,600,on_contour_trackbar)
    cv2.createTrackbar('canny_lo','config',67,600,on_contour_trackbar)
    cv2.createTrackbar('medianBlur','config',2,15,on_filter_trackbar)
    cv2.setMouseCallback('floodfill',onMouse)
          
    new_flood = True
    final_mask = prepare_image()

    while True:
        if cv2.getTrackbarPos('debug','config') >= 2:
            cv2.imshow('img',img)
        if cv2.getTrackbarPos('debug','config') >= 1:
            cv2.imshow('final_img',final_mask)
        key = cv2.waitKey(15)
        if key == ord('g'):#guarda la imagen en bn para la comparacion
            return [final_mask,img]
            break
        if key == ord('f'):
            fixed_range = not fixed_range
        if key == ord('c'):
            connectivity = 12-connectivity
        if key == ord('k'):#reestablece todos los valores a los nuevos que hayamos elegido
            new_flood = True
            seed_pt = None
            prepare_image()
            
        if key == 27:
            break
    
    



if __name__ == "__main__":
    print help_message

    images_name = sys.argv[1:]
    binary_images = []



    for img_name in images_name :

        img = cv2.imread(img_name)#butterflies_resize
        binary_images = binary_images + [calcMask(img)]
        
        

