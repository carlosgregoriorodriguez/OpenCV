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

def compare():
    global j
        
    imToShow = []
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

            for i in range(len(v)):
                if v[i]< eps[i]:
                    break
                elif i == len(v)-1:
                    cv2.putText(img,str(v),(50,img.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))  
                    imToShow = imToShow+[img]
        else :
            eps = [(cv2.getTrackbarPos('CHI---epsB','config2')/10.0),(cv2.getTrackbarPos('CHI---epsG','config2')/10.0),(cv2.getTrackbarPos('CHI---epsR','config2')/10.0)]
            v1 = cv2.compareHist(histB, histB1, cv2.cv.CV_COMP_CHISQR)
            v2 = cv2.compareHist(histG, histG1, cv2.cv.CV_COMP_CHISQR)
            v3 = cv2.compareHist(histR, histR1, cv2.cv.CV_COMP_CHISQR) 
            v = [v1, v2, v3]
            
            for i in range(len(v)):
                if v[i]> eps[i]:
                    break
                elif i == len(v)-1:
                    cv2.putText(img,str(v),(50,img.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))
                    imToShow = imToShow+[img]

        j = 1
        for im in imToShow:
            cv2.imshow('im_'+str(j),im)
            j = j+1
            
    


if __name__ == "__main__":
    print help_message

    images_name = sys.argv[1:]
    compare_images = []


#########   STEP 1   ###########################

    for img_name in images_name :
        img = cv2.imread(img_name)
        compare_images = compare_images + [calcBinaryImage2.calcMask(img)]


################  STEP2   #######################

    cv2.destroyAllWindows()

    print '''

 STEP 2 (comparison)
  s    -   look for the more similar images with the chosen data
  q    -   EXIT
  c    -   change histogram comparison method

'''

    chi = True

    cv2.namedWindow('config2')
    cv2.createTrackbar('CORR---epsB','config2',10,20,dummy)
    cv2.createTrackbar('CORR---epsG','config2',10,20,dummy)
    cv2.createTrackbar('CORR---epsR','config2',10,20,dummy)
    cv2.createTrackbar('CHI---epsB','config2',100,200,dummy)
    cv2.createTrackbar('CHI---epsG','config2',100,200,dummy)
    cv2.createTrackbar('CHI---epsR','config2',100,200,dummy)
   
    pimg = compare_images[0][1]
    histB = cv2.calcHist([cv2.split(pimg)[0]],[0],compare_images[0][0],[256],[0,255])
    cv2.normalize(histB,histB,0,1,cv2.NORM_MINMAX)
    histG = cv2.calcHist([cv2.split(pimg)[1]],[0],compare_images[0][0],[256],[0,255])
    cv2.normalize(histG,histG,0,1,cv2.NORM_MINMAX)
    histR = cv2.calcHist([cv2.split(pimg)[2]],[0],compare_images[0][0],[256],[0,255])
    cv2.normalize(histR,histR,0,1,cv2.NORM_MINMAX) 
     
    compare()

    while True:
        cv2.imshow('image',pimg)
        key = cv2.waitKey(5)
        if key == ord('s'):
            for k in range(j):
                cv2.destroyWindow('im_'+str(k))
            cv2.imshow('image',pimg)
            compare()
        if key == ord('c'):
            chi = not chi
            if chi:
                print 'chi square'
            else:
                print 'correlation'
        if key == ord('q'):
            break
    
