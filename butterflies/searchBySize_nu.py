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
    for k in range(j):
        cv2.destroyWindow('im_mask_'+str(k))
    for k in range(len(compare_images)+1):
        cv2.destroyWindow('image'+str(k))
    # compare with new data
    compareMoments(nu, compare_images, cv2.getTrackbarPos('show all input images', 'config2'), cv2.getTrackbarPos('show all selected masks','config2'))

def onMaskImages(pos):
    # shows all mask of compare_images
    if pos != 0:
        i = 1
        for img in compare_images:
            h = int(img[0].shape[0]*0.75)
            w = int(img[0].shape[1]*0.75)
            if pos == 2:# resize the image
                copy_img = cv2.resize(img[0], (w,h))
            else:
                copy_img = img[0]
            cv2.imshow('mask_image_'+str(i),copy_img)
            i = i+1
    # remove all previous shown masks
    if pos == 0:
        for i in range(len(compare_images)+1):
            cv2.destroyWindow('mask_image_'+str(i))
                
def dummy(pos):
    a = pos

def compareMoments(H,compare_images, showAllImages=0, showSelectMask=0):
    global j
    # takes epsilon values of trackbar 
    eps = [cv2.getTrackbarPos('eps1','config2')*10**(-3),cv2.getTrackbarPos('eps2','config2')*10**(-3),cv2.getTrackbarPos('eps3','config2')*10**(-3),cv2.getTrackbarPos('eps4','config2')*10**(-3),cv2.getTrackbarPos('eps5','config2')*10**(-3),cv2.getTrackbarPos('eps6','config2')*10**(-3), cv2.getTrackbarPos('eps7(area)','config2')]
    print eps
    # for each img in compare_images calculates its Hu moments and compare it with the moments of original image
    imshow = []
    returnImg = []
    j = 1
    for im in compare_images:
        mask = im[0]
        img = im[1]
        moments1 = cv2.moments(mask,True)
        nu1 = [moments1['nu02']] + [moments1['nu11']] + [moments1['nu12']] + [moments1['nu20']] + [moments1['nu21']] + [moments1['nu30']] + [moments1['m00']]
        #print nu1
        H1 = cv2.HuMoments(moments1)
        cv2.putText(img,str(nu1[0:2]),(50,mask.shape[0]-100),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
        cv2.putText(img,str(nu1[2:4]),(50,mask.shape[0]-75),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
        cv2.putText(img,str(nu1[4:6]),(50,mask.shape[0]-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
        cv2.putText(img,str(nu1[6:]),(50,mask.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
        
        # if showAllImages!=0 then want show all compare_images
        if showAllImages==2:# shows resize image
            copy_img = cv2.resize(img, (int(mask.shape[1]*0.75), int(mask.shape[0]*0.75)))
            cv2.imshow('image'+str(j),copy_img)
            j = j+1
        if showAllImages==1:# shows real image
            cv2.imshow('image'+str(j),img)
            j = j+1
       

        # if a value of H1 is not equals to its corresponding in H (more or less epsilon) not keep looking
        for i in range(len(H)):
            if H[i]> nu1[i]+eps[i] or H[i]<nu1[i]-eps[i]:
                break 
            elif i == len(H)-1:
                imshow = imshow+[[mask,img,im[2]]]
                returnImg = returnImg + [im]

    # shows all selected images
    j = 1
    for im in imshow:
        cv2.imshow('im_'+str(j),im[1])
        if showSelectMask == 1:# show selected image mask
            cv2.imshow('im_mask_'+str(j),im[0])
        j = j+1
    return returnImg

def findMask(images_name):
     # for each image calculates its mask
    compare_images = []
    for img_name in images_name :
        img = cv2.imread(img_name)
        compare_images = compare_images + [calcBinaryImage2.calcMask(img,img_name)]
    return compare_images

def compareBySize(compareImages):
    global H,compare_images,nu
    print help_message
    
    compare_images = compareImages
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
    cv2.createTrackbar('eps1','config2',100,1000,dummy)
    cv2.createTrackbar('eps2','config2',50,1000,dummy)
    cv2.createTrackbar('eps3','config2',25,1000,dummy)
    cv2.createTrackbar('eps4','config2',150,1000,dummy)
    cv2.createTrackbar('eps5','config2',150,1000,dummy)
    cv2.createTrackbar('eps6','config2',150,1000,dummy)
    cv2.createTrackbar('eps7(area)','config2',150,5000,dummy)
    cv2.createTrackbar('show all input images', 'config2',0,2,onShowImages)
    cv2.createTrackbar('show all masks','config2', 0,2,onMaskImages)
    cv2.createTrackbar('show all selected masks','config2', 0,1,onShowImages)

    # selects main image for comparison and calculates its moments
    pimg = compare_images[0][0]
    img = compare_images[0][1].copy()
    moments = cv2.moments(pimg,True)
    #print moments
    nu = [moments['nu02']] + [moments['nu11']] + [moments['nu12']] + [moments['nu20']] + [moments['nu21']] + [moments['nu30']] + [moments['m00']]
    #print nu
    H = cv2.HuMoments(moments)

    cv2.putText(img,str(nu[0:2]),(50,img.shape[0]-100),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
    cv2.putText(img,str(nu[2:4]),(50,img.shape[0]-75),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
    cv2.putText(img,str(nu[4:6]),(50,img.shape[0]-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
    cv2.putText(img,str(H[6:]),(50,img.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
   
    # compares pimg moments with all other images moments
    returnImg = compareMoments(nu,compare_images,0,0)

    while True:
        cv2.imshow('image',img)
        key = cv2.waitKey(5)
        # removes old windows and calculates the most similar images with the new values
        if key == ord('s'):
            for k in range(j):
                cv2.destroyWindow('im_'+str(k))
                cv2.destroyWindow('im_mask_'+str(k))
            for k in range(len(compare_images)+1):
                cv2.destroyWindow('image'+str(k))
            cv2.imshow('image',img)
            returnImg = compareMoments(nu,compare_images,cv2.getTrackbarPos('show all input images','config2'), cv2.getTrackbarPos('sohw all selected masks','config2'))
        # EXIT
        if key == ord('q'):
            return returnImg 

def compare(images_name):
    compare_images = findMask(images_name)
    selectedImages = compareBySize(compare_images)
    return selectedImages


if __name__ == "__main__":

    images_name = sys.argv[1:]
    
    compare(images_name)

        
