#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np
import calcBinaryImage2

help_message = '''USAGE: searchByColor.py [<image for compare>,<image>,...]

Keys:

 STEP 1
  g    -   save the binary image for later comparison
  k    -   reset the values chosen for the image
  ESC  -   moves to the next image for analyzing

'''

def dummy(pos):
    a = pos

def onShowImages(pos=None):
    # destroy old windows
    for k in range(j):
        cv2.destroyWindow('im_mask_'+str(k))
    for k in range(len(compare_images)+1):
        cv2.destroyWindow('image'+str(k))
    # compare with new data
    compare(compare_images, histB, histG, histR, chi, cv2.getTrackbarPos('show all input images', 'config2'), cv2.getTrackbarPos('show all selected masks','config2'))

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


def compare(compare_images, histB, histG, histR, chi,showAllImages=0, showSelectMask=0):
    global j
    
    # for each im in compare_images calculates its histograms and compare ir with the histograms of original image
    imToShow = []
    j = 1
    for im in compare_images:
        img = im[1]
        histB1 = cv2.calcHist([cv2.split(img)[0]],[0],im[0],[256],[0,255])
        cv2.normalize(histB1,histB1,0,1,cv2.NORM_MINMAX)
        histG1 = cv2.calcHist([cv2.split(img)[1]],[0],im[0],[256],[0,255])
        cv2.normalize(histG1,histG1,0,1,cv2.NORM_MINMAX)
        histR1 = cv2.calcHist([cv2.split(img)[2]],[0],im[0],[256],[0,255])
        cv2.normalize(histR1,histR1,0,1,cv2.NORM_MINMAX)
            
        if not chi:
            eps = [cv2.getTrackbarPos('CORR---epsB','config2')/10.0-1,cv2.getTrackbarPos('CORR---epsG','config2')/10.0-1,cv2.getTrackbarPos('CORR---epsR','config2')/10.0-1]
            v1 = cv2.compareHist(histB, histB1, cv2.cv.CV_COMP_CORREL)
            v2 = cv2.compareHist(histG, histG1, cv2.cv.CV_COMP_CORREL)
            v3 = cv2.compareHist(histR, histR1, cv2.cv.CV_COMP_CORREL)
            v = [v1, v2, v3]
            
            image = img.copy()
            cv2.putText(image,str(v),(50,img.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))

            # if showAllImages!=0 then want show all compare_images
            if showAllImages==2:# shows resize image
                copy_img = cv2.resize(image, (int(img.shape[1]*0.75), int(img.shape[0]*0.75)))
                cv2.imshow('image'+str(j),copy_img)
                j = j+1
            if showAllImages==1:# shows real image
                cv2.imshow('image'+str(j),image)
                j = j+1

            # if a value of v is not lesser epsilon then not keep looking
            for i in range(len(v)):
                if v[i]< eps[i]:
                    break
                elif i == len(v)-1:  
                    imToShow = imToShow+[[im[0],image]]
                    
        else :
            eps = [(cv2.getTrackbarPos('CHI---epsB','config2')/10.0),(cv2.getTrackbarPos('CHI---epsG','config2')/10.0),(cv2.getTrackbarPos('CHI---epsR','config2')/10.0)]
            v1 = cv2.compareHist(histB, histB1, cv2.cv.CV_COMP_CHISQR)
            v2 = cv2.compareHist(histG, histG1, cv2.cv.CV_COMP_CHISQR)
            v3 = cv2.compareHist(histR, histR1, cv2.cv.CV_COMP_CHISQR) 
            v = [v1, v2, v3]

            image = img.copy()
            cv2.putText(image,str(v),(50,img.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))

            # if showAllImages!=0 then want show all compare_images
            if showAllImages==2:# shows resize image
                copy_img = cv2.resize(image, (int(img.shape[1]*0.75), int(img.shape[0]*0.75)))
                cv2.imshow('image'+str(j),copy_img)
                j = j+1
            if showAllImages==1:# shows real image
                cv2.imshow('image'+str(j),image)
                j = j+1

            # if a value of v is not lesser epsilon then not keep looking
            for i in range(len(v)):
                if v[i]> eps[i]:
                    break
                elif i == len(v)-1:
                    imToShow = imToShow+[[im[0],image]]

    # shows all selected images
    j = 1
    for im in imToShow:
        cv2.imshow('im_'+str(j),im[1])
        if showSelectMask == 1:# show selected image mask
            cv2.imshow('im_mask_'+str(j),im[0])
        j = j+1

    return imToShow

def compareByColor(images_name): 
    global compare_images, chi, histB,histG, histR
    print help_message 
    compare_images = []

    ##########   STEP 1   #####################
 
    # for each image calculates its mask
    for img_name in images_name :
        img = cv2.imread(img_name)
        compare_images = compare_images + [calcBinaryImage2.calcMask(img)]


    ##########  STEP2   #######################

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
  c    -   change histogram comparison method

'''                      
    chi = True

    # creates config window with its trackbars
    cv2.namedWindow('config2')
    cv2.createTrackbar('CORR---epsB','config2',10,20,dummy)
    cv2.createTrackbar('CORR---epsG','config2',10,20,dummy)
    cv2.createTrackbar('CORR---epsR','config2',10,20,dummy)
    cv2.createTrackbar('CHI---epsB','config2',100,200,dummy)
    cv2.createTrackbar('CHI---epsG','config2',100,200,dummy)
    cv2.createTrackbar('CHI---epsR','config2',100,200,dummy)
    cv2.createTrackbar('show all input images', 'config2',0,2,onShowImages)
    cv2.createTrackbar('show all masks','config2', 0,2,onMaskImages)
    cv2.createTrackbar('show all selected masks','config2', 0,1,onShowImages)
   

    # selects main image for comparison and calculates its histograms
    pimg = compare_images[0][1]
    histB = cv2.calcHist([cv2.split(pimg)[0]],[0],compare_images[0][0],[256],[0,255])
    cv2.normalize(histB,histB,0,1,cv2.NORM_MINMAX)
    histG = cv2.calcHist([cv2.split(pimg)[1]],[0],compare_images[0][0],[256],[0,255])
    cv2.normalize(histG,histG,0,1,cv2.NORM_MINMAX)
    histR = cv2.calcHist([cv2.split(pimg)[2]],[0],compare_images[0][0],[256],[0,255])
    cv2.normalize(histR,histR,0,1,cv2.NORM_MINMAX) 
     
  
    # compares pimg histograms with all other images histograms
    imToShow = compare(compare_images, histB, histG, histR, chi)

    while True:
        cv2.imshow('image',pimg)
        key = cv2.waitKey(5)
        # removes old windows and calculates the most similar images with the new values
        if key == ord('s'):
            for k in range(j):
                cv2.destroyWindow('im_'+str(k))
                cv2.destroyWindow('im_mask_'+str(k))
            for k in range(len(compare_images)+1):
                cv2.destroyWindow('image'+str(k))
            cv2.imshow('image',pimg)
            imToShow = compare(compare_images, histB, histG, histR, chi)
        if key == ord('c'):
            chi = not chi
            if chi:
                print 'chi square'
            else:
                print 'correlation'
        # EXIT
        if key == ord('q'):
            return imToShow
  


if __name__ == "__main__":

    images_name = sys.argv[1:]

    compareByColor(images_name)
