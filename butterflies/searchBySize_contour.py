#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
import numpy as np
import calcBinaryImage2

help_message = '''USAGE: searchBySize_contour.py [<image for compare>,<image>,...]

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
    compareContours(buttContours, compare_images,cv2.getTrackbarPos('show all input images', 'config2'), cv2.getTrackbarPos('show all selected masks','config2') )

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

# finds butterfly's contour
def findButtContour(mask_img,real_img):
    
    # calculates butterfly area with moments (the number of "white" pixels)
    moments = cv2.moments(mask_img, True)
    area = moments['m00']

    #img_erode = cv2.erode(mask_img, kernel=None, iterations=3)

    # calculates contours
    img_canny = cv2.Canny(mask_img, 45, 134)
    contours, hier = cv2.findContours(img_canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cv2.approxPolyDP(contour, 1, True) for contour in contours]

    # for each contour, checks if is the butterfly's contour
    butt_contour = [np.array(0),None,0]
    for i in range(len(contours)):
        #img_copy = real_img.copy()
        cont_area = cv2.contourArea(contours[i])
       # cv2.drawContours(img_copy,contours,i, (0,255,255),1,cv2.CV_AA)
        
        # if cont_area is similar to area then save this contour and stop looking
        if cont_area > area-area/2:
            butt_contour = [contours[i],i,area]
            print 'real_area: ',area,'  cont_area: ',cont_area
            break
        else:
            # calculates minEnclosingCircle and boundingRect, keeps the minimum of these and compares this area (area_comp) with the butterfly's contour area
            center, radius = cv2.minEnclosingCircle(contours[i])
            rect = cv2.boundingRect(contours[i])
            area_circle = radius*radius*np.pi
            area_rect = rect[2]*rect[3]
            area_comp = min(area_circle, area_rect)
            print 'area_circle: ',area_circle,'  area_rect: ', area_rect,'  real_area: ', area, '  cont_area: ',cont_area
            # if area_comp is similar to area then save this contour and stop looking
            if area_comp<area+area and area_comp>area-area/2:
                butt_contour = [contours[i],i,area]
                
    print 'contour... ',butt_contour[1], butt_contour[2]
    img_copy = real_img.copy()
    if butt_contour[1] != None:
        cv2.drawContours(img_copy,contours,butt_contour[1], (255,0,255),1,cv2.CV_AA)
    cv2.imshow('final',img_copy)
    cv2.waitKey(0)
    cv2.destroyWindow('final')
    return butt_contour

def compareContours(buttContours, compare_images, showAllImages=0, showSelectMask=0):
    imSelect = []
    returnImg = []
    principalContour = buttContours[0][0]
    for i in range(len(buttContours)):

        # if showAllImages!=0 then want show all compare_images
        if showAllImages==1:# shows real image
            cv2.imshow(str(compare_images[i][2]),compare_images[i][1])

        # compare contours with matchShapes
        if buttContours[i][1]==None:
            print '¡¡¡¡¡¡¡¡¡¡ not found this contour ('+str(compare_images[i][2])+') !!!!!!!!!!!'
        else:
            comp1 = cv2.matchShapes(principalContour, buttContours[i][0], cv2.cv.CV_CONTOURS_MATCH_I1,0)
            comp2 = cv2.matchShapes(principalContour, buttContours[i][0], cv2.cv.CV_CONTOURS_MATCH_I2,0)
            comp3 = cv2.matchShapes(principalContour, buttContours[i][0], cv2.cv.CV_CONTOURS_MATCH_I3,0)


        # compare contours with alternative moments
        if buttContours[i][1] != None:
            contour = buttContours[i][0]
            area = buttContours[i][2]
            x,y,w,h = cv2.boundingRect(contour)
            aspect_ratio = float(w)/h
            equi_diameter = np.sqrt(4*area/np.pi)
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)
            hull_defects = np.abs(hull_area-area)
            c,r = cv2.minEnclosingCircle(contour)
            circle_area = r*r*np.pi
            circle_defects = np.abs(circle_area-area)

        copy = compare_images[i][1].copy()
        cv2.putText(copy,'['+str(comp1)+', '+str(comp2)+', '+str(comp3)+']',(50,copy.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
        cv2.putText(copy, '['+str(aspect_ratio)+', '+str(equi_diameter)+', '+str(hull_defects)+', '+str(circle_defects)+']',(50,copy.shape[0]-50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))

        if comp1<cv2.getTrackbarPos('eps-I1','config2')/100.0 and comp2<cv2.getTrackbarPos('eps-I2','config2')/100.0 and comp3<cv2.getTrackbarPos('eps-I3','config2')/100.0:
            imSelect = imSelect + [[compare_images[i][0],copy,compare_images[i][2]]]
            returnImg = returnImg + [compare_images[i]]

    # shows selected images
    for img in imSelect:
        cv2.imshow('selected_'+str(img[2]),img[1])
        if showSelectMask == 1:# show selected image mask
            cv2.imshow('im_mask_'+str(img[2]),img[0])
    return returnImg

def findMask(images_name):
     # for each image calculates its mask
    print help_message
    compare_images = []
    for img_name in images_name :
        img = cv2.imread(img_name)
        compare_images = compare_images + [calcBinaryImage2.calcMask(img,img_name)]
    return compare_images

def compareBySize(compareImages):
    global buttContours,compare_images
    
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
    cv2.createTrackbar('eps_cont_area','config2',10000,20000,dummy)
    cv2.createTrackbar('eps-I1','config2',10,100,dummy)
    cv2.createTrackbar('eps-I2','config2',100,500,dummy)
    cv2.createTrackbar('eps-I3','config2',10,100,dummy)
    cv2.createTrackbar('show all input images', 'config2',0,1,onShowImages)
    cv2.createTrackbar('show all masks','config2', 0,2,onMaskImages)
    cv2.createTrackbar('show all selected masks','config2', 0,1,onShowImages)

    '''
    # selects main image for comparison and calculates its moments
    mask_img = compare_images[0][0]
    real_img = compare_images[0][1]
    print type(mask_img), mask_img.dtype
    #mask_img = cv2.imread('mask_BMC-1968_D.jpg',-1)
    #print type(mask_img), mask_img.dtype
    '''

    buttContours = []
    for img in compare_images:
        mask_img = img[0]
        real_img = img[1]
        buttContours = buttContours + [np.array(findButtContour(mask_img,real_img))]
        
    selectedImages = compareContours(buttContours, compare_images)
        
    '''
    print "comparando contornos 2 y 3", cv2.matchShapes(contours[2], contours[3], cv2.cv.CV_CONTOURS_MATCH_I1,0)
    print "comparando contornos 2 y 3", cv2.matchShapes(contours[2], contours[3], cv2.cv.CV_CONTOURS_MATCH_I2,0)
    print "comparando contornos 2 y 3", cv2.matchShapes(contours[2], contours[3], cv2.cv.CV_CONTOURS_MATCH_I3,0)
    print "comparando contornos 1 y 3", cv2.matchShapes(contours[1], contours[3], cv2.cv.CV_CONTOURS_MATCH_I1,0)
    print "comparando contornos 1 y 3", cv2.matchShapes(contours[1], contours[3], cv2.cv.CV_CONTOURS_MATCH_I2,0)
    print "comparando contornos", cv2.matchShapes(contours[1], contours[3], cv2.cv.CV_CONTOURS_MATCH_I3,0)
    '''    
   
    while True:
        cv2.imshow(str(compare_images[0][2]),compare_images[0][1])
        key = cv2.waitKey(5)
        # removes old windows and calculates the most similar images with the new values
        if key == ord('s'):
            for im in compare_images:
                cv2.destroyWindow('selected_'+str(im[2]))
                cv2.destroyWindow('im_mask_'+str(im[2]))
                cv2.destroyWindow(str(im[2]))
            cv2.imshow(str(compare_images[0][2]),compare_images[0][1])
            selectedImages = compareContours(buttContours, compare_images,cv2.getTrackbarPos('show all input images', 'config2'), cv2.getTrackbarPos('show all selected masks','config2'))
        # EXIT
        if key == ord('q'):
            cv2.destroyWindow('config2')
            for im in compare_images:
                cv2.destroyWindow('selected_'+str(im[2]))
                cv2.destroyWindow('im_mask_'+str(im[2]))
                cv2.destroyWindow(str(im[2]))
            return selectedImages

def compare(images_name):
    compare_images = findMask(images_name)
    selectedImages = compareBySize(compare_images)
    return selectedImages
    


if __name__ == "__main__":

    images_name = sys.argv[1:]
    
    compare(images_name)

        
