#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np

help_message = '''USAGE: floodfillgray.py [<image for compare>,<image>,...]

Keys:

 STEP 1
  g    -   save the binary image for later comparison
  k    -   reset the values chosen for the image
  ESC  -   moves to the next image for analyzing

'''

def dummy(pos):
    a = pos

def onMouse(event, x, y, flag, param):
    global seed_pt
    if flag & cv2.EVENT_FLAG_LBUTTON:
        seed_pt = x, y
        update()

def update():
    global img, img_but, reduced_img, seed_pt, connectivity, flood, reduced_img2,point, img_thres
    img2 = img.copy()
    img_but2 = img_but.copy()
    if flood:
        red = reduced_img
        seed_pt = None
    else:
        red = reduced_img2
    
    
    mb = cv2.getTrackbarPos('medianBlur','config')
    if (mb%2 != 0):
        img_but2 = cv2.medianBlur(img_but2,mb)
    else:
        img_but2 = cv2.medianBlur(img_but2,mb-1)
    #cv2.imshow('median_blur',img_but2)
        
    it = cv2.getTrackbarPos('erode_it','config')
    img_erode = cv2.erode(img_but2, kernel=None, iterations = 3)
    #cv2.imshow('erode',img_erode)
    
    imgbn = cv2.cvtColor(img_erode,cv2.cv.CV_BGR2GRAY)
    canny = cv2.Canny(imgbn,cv2.getTrackbarPos('canny_hi(1)','config'),cv2.getTrackbarPos('canny_lo(1)','config'))
    #cv2.imshow('canny(1)',canny)
    rawcontours,hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);
    cv2.drawContours(img_but2, rawcontours, -1, (255,0,0), 1, cv2.CV_AA)
    if flood:
        red[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = img_but2

        flood = False

    mask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)
    mask[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = canny
        
    if seed_pt !=  None:
        flags = connectivity
        if fixed_range:
            flags |= cv2.FLOODFILL_FIXED_RANGE
        cv2.floodFill(red, mask, seed_pt, (255, 255, 255), (cv2.getTrackbarPos('floodfill_lo','config'),)*3, (cv2.getTrackbarPos('floodfill_hi','config'),)*3, flags)

    cv2.floodFill(red, mask, (point[0]+128,point[1]-6), (255, 255, 255), (3,)*3, (60,)*3, flags=4)
    cv2.floodFill(red, mask, (point[0]+11,point[1]-6), (255, 255, 255), (2,)*3, (100,)*3)
    cv2.floodFill(red, mask, (point[0]+point[1]+int(2*point[1]/3)-20,10), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
    cv2.floodFill(red, mask, (point[0]+15,point[1]-38), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
        
    reduced_img2 = red
    cv2.imshow('floodfill',red)    
    imgbn = cv2.cvtColor(red,cv2.cv.CV_BGR2GRAY)

    retVal,img_thres = cv2.threshold(imgbn,cv2.getTrackbarPos('threshold','config'),255,cv2.THRESH_BINARY_INV)
    cv2.imshow('thres',img_thres)
    
    


if __name__ == "__main__":
    print help_message

    images_name = sys.argv[1:]
    template = cv2.imread('qp.jpg')
    compare_images = []




#########   STEP 1   ###########################


    cv2.namedWindow('config')
    cv2.namedWindow('floodfill')
    cv2.createTrackbar('floodfill_hi','config',60,255,dummy)
    cv2.createTrackbar('floodfill_lo','config',10,255,dummy)
    cv2.createTrackbar('canny_hi(1)','config',144,600,dummy)
    cv2.createTrackbar('canny_lo(1)','config',67,600,dummy)
    cv2.createTrackbar('canny_hi(2)','config',48,600,dummy)
    cv2.createTrackbar('canny_lo(2)','config',22,600,dummy)
    cv2.createTrackbar('medianBlur','config',2,15,dummy)
    cv2.createTrackbar('threshold','config',254,255,dummy)

    cv2.setMouseCallback('floodfill',onMouse)


    for img_name in images_name :
       
        connectivity = 4
        fixed_range = True
        flood = True

        img = cv2.imread(img_name)#butterflies_resize

        img_thres = img
        imgfound = cv2.matchTemplate(img,template, cv2.TM_SQDIFF_NORMED)
        minV,maxV,minL,maxL = cv2.minMaxLoc(imgfound)
        point = (minL[0], minL[1]-35)
        seed_pt = None
        
        reduced_img = np.zeros(img.shape,np.uint8)+255
        reduced_img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)] = img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)]
        
        img_but = img[0:point[1]-5, point[0]+10:point[0]+point[1]+int(2*point[1]/3)]
        reduced_img2 = reduced_img.copy()
        update()
        

        while True:
            img3 = img.copy()
            cv2.imshow('img',img3)
            key = cv2.waitKey(5)
            if key == ord('g'):#guarda la imagen en bn para la comparacion
                compare_images = compare_images + [[img_thres,img]]
                break
            if key == ord('f'):
                fixed_range = not fixed_range
            if key == ord('c'):
                connectivity = 12-connectivity
            if key == ord('k'):#reestablece todos los valores a los nuevos que hayamos elegido
                flood = True
            if key == 27:
                break
            update()



################  STEP2   #####################################

    cv2.destroyAllWindows()

    print '''

 STEP 2 (comparison)
  s    -   look for the more similar images with the chosen data
  q    -   EXIT

'''


    chi = True

    cv2.namedWindow('config2')
    cv2.createTrackbar('CORR---epsB','config2',10,20,dummy)
    cv2.createTrackbar('CORR---epsG','config2',10,20,dummy)
    cv2.createTrackbar('CORR---epsR','config2',10,20,dummy)
    cv2.createTrackbar('CHI---epsB','config2',100,100,dummy)
    cv2.createTrackbar('CHI---epsG','config2',100,100,dummy)
    cv2.createTrackbar('CHI---epsR','config2',100,100,dummy)
   
    pimg = compare_images[0][1]
    histB = cv2.calcHist([cv2.split(pimg)[0]],[0],compare_images[0][0],[256],[0,255])
    cv2.normalize(histB,histB,0,1,cv2.NORM_MINMAX)
    histG = cv2.calcHist([cv2.split(pimg)[1]],[0],compare_images[0][0],[256],[0,255])
    cv2.normalize(histG,histG,0,1,cv2.NORM_MINMAX)
    histR = cv2.calcHist([cv2.split(pimg)[2]],[0],compare_images[0][0],[256],[0,255])
    cv2.normalize(histR,histR,0,1,cv2.NORM_MINMAX)

    
   
    def update2():
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
                        imToShow = imToShow+[img]


        j = 1
        for im in imToShow:
            cv2.imshow('im_'+str(j),im)
            j = j+1
            

    update2()
    while True:
        cv2.imshow('image',pimg)
        key = cv2.waitKey(5)
        if key == ord('s'):
            for k in range(j):
                cv2.destroyWindow('im_'+str(k))
            cv2.imshow('image',pimg)
            update2()
        if key == ord('c'):
            chi = not chi
            if chi:
                print 'chi square'
            else:
                print 'correlation'
        if key == ord('q'):
            break
    
   
