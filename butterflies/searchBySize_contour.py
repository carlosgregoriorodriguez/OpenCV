#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np
import calcBinaryImage2

help_message = '''USAGE: searchBySize.py [<image for compare>,<image>,...]

Keys:

 STEP 1
  g    -   save the binary image for later comparison
  k    -   reset the values chosen for the image
  ESC  -   moves to the next image for analyzing

'''  

def onShowImages(pos=None):
    # destroy old windows
    for im in compare_images:
        cv2.destroyWindow('im_mask_'+str(im[2]))
        cv2.destroyWindow(str(im[2]))
    # compare with new data
    compare(nu, compare_images, cv2.getTrackbarPos('show all input images', 'config2'), cv2.getTrackbarPos('show all selected masks','config2'))

def onMaskImages(pos):
    # shows all mask of compare_images
    if pos != 0:
        i = 1
        for im in compare_images:
            h = int(im[0].shape[0]*0.75)
            w = int(im[0].shape[1]*0.75)
            if pos == 2:# resize the image
                copy_img = cv2.resize(im[0], (w,h))
            else:
                copy_img = im[0]
            cv2.imshow('mask_image_'+str(im[2]),copy_img)
            i = i+1
    # remove all previous shown masks
    if pos == 0:
        for im in compare_images:
            cv2.destroyWindow('mask_image_'+str(im[2]))
                
def dummy(pos):
    a = pos

def compareBySize(images_name):
    global H,compare_images,nu
    print help_message

    ######### STEP 1 #################

    # for each image calculates its mask
    compare_images = []
    for img_name in images_name :
        img = cv2.imread(img_name)
        compare_images = compare_images + [calcBinaryImage2.calcMask(img,img_name)]
        
    ######## STEP 2 ##################
    
    # destroy old windows
    cv2.destroyWindow('config')
    cv2.destroyWindow('floodfill')
    cv2.destroyWindow('median_blur')
    cv2.destroyWindow('erode')
    cv2.destroyWindow('final_img')
    cv2.destroyWindow('img')
    cv2.destroyWindow('canny')

    print '''

 STEP 2 (comparison)
  s    -   look for the more similar images with the chosen data
  q    -   EXIT

'''

    # creates config window with its trackbars
    cv2.namedWindow('config2')
    cv2.createTrackbar('eps_cont_area','config2',1500,5000,dummy)
    cv2.createTrackbar('show all input images', 'config2',0,2,onShowImages)
    cv2.createTrackbar('show all masks','config2', 0,2,onMaskImages)
    cv2.createTrackbar('show all selected masks','config2', 0,1,onShowImages)

    # selects main image for comparison and calculates its moments
    mask_img = compare_images[0][0]
    print type(mask_img), mask_img.dtype
    #mask_img = cv2.imread('mask_BMC-1968_D.jpg',-1)
    #print type(mask_img), mask_img.dtype
    
    real_img = compare_images[0][1]
    moments = cv2.moments(mask_img, True)
    area = moments['m00']

    img_erode = cv2.erode(mask_img, kernel=None, iterations=3)
    img_canny = cv2.Canny(img_erode, 45, 134)
    cv2.imshow("canny", img_canny)

    contours, hier = cv2.findContours(img_canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cv2.approxPolyDP(contour, 1, True) for contour in contours]
    print len(contours)
    cv2.drawContours(real_img,contours,-1,(255,0,0),1, cv2.CV_AA)
    for i in range(len(contours)):
        #print contours[i]
        img_copy = real_img.copy()
        cv2.drawContours(img_copy,contours,i, (0,0,255),1,cv2.CV_AA)
        cont_area = cv2.contourArea(contours[i])
        print 'area... ',cont_area
        cv2.imshow('im',img_copy)
        cv2.waitKey(0)
        
        if cont_area > area-cv2.getTrackbarPos('eps_cont_area','config2'):
            butt_contour = contours[i]
    print "comparando contornos 2 y 3", cv2.matchShapes(contours[2], contours[3], cv2.cv.CV_CONTOURS_MATCH_I1,0)
    print "comparando contornos 2 y 3", cv2.matchShapes(contours[2], contours[3], cv2.cv.CV_CONTOURS_MATCH_I2,0)
    print "comparando contornos 2 y 3", cv2.matchShapes(contours[2], contours[3], cv2.cv.CV_CONTOURS_MATCH_I3,0)
    print "comparando contornos 1 y 3", cv2.matchShapes(contours[1], contours[3], cv2.cv.CV_CONTOURS_MATCH_I1,0)
    print "comparando contornos 1 y 3", cv2.matchShapes(contours[1], contours[3], cv2.cv.CV_CONTOURS_MATCH_I2,0)
    print "comparando contornos", cv2.matchShapes(contours[1], contours[3], cv2.cv.CV_CONTOURS_MATCH_I3,0)
        
   
    while True:
        cv2.imshow('image',img)
        key = cv2.waitKey(5)
        # removes old windows and calculates the most similar images with the new values
        if key == ord('s'):
            for im in compare_images:
                cv2.destroyWindow('im_'+str(im[2]))
                cv2.destroyWindow('im_mask_'+str(im[2]))
                cv2.destroyWindow('selected_'+str(im[2]))
            cv2.imshow('image',img)
        # EXIT
        if key == ord('q'):
            return



if __name__ == "__main__":

    images_name = sys.argv[1:]
    
    compareBySize(images_name)

        
