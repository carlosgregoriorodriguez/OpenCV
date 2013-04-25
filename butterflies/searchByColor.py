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
    for img in compare_images:
        cv2.destroyWindow('im_mask_'+str(img[2]))
        cv2.destroyWindow(str(img[2]))
    # compare with new data
    compareHist(compare_images, histB, histG, histR, chi, show_hist, cv2.getTrackbarPos('show all input images', 'config2'), cv2.getTrackbarPos('show all selected masks','config2'))

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
            cv2.imshow('mask_image_'+str(img[2]),copy_img)
            i = i+1
    # remove all previous shown masks
    if pos == 0:
        for img in compare_images:
            cv2.destroyWindow('mask_image_'+str(img[2]))


def compareHist(compare_images, histB, histG, histR, chi = True, showHist = True, showAllImages=0, showSelectMask=0):
    global j
    
    # for each im in compare_images calculates its histograms and compare ir with the histograms of original image
    imToShow = []
    returnImg = []
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
                cv2.imshow(str(im[2]),copy_img)
                j = j+1
            if showAllImages==1:# shows real image
                cv2.imshow(str(im[2]),image)
                j = j+1

            # if a value of v is not lesser epsilon then not keep looking
            for i in range(len(v)):
                if v[i]< eps[i]:
                    break
                elif i == len(v)-1:  
                    imToShow = imToShow+[[im[0],image,im[2]]]
                    returnImg = returnImg + [im]
                    
        else :
            eps = [(cv2.getTrackbarPos('CHI---epsB','config2')),(cv2.getTrackbarPos('CHI---epsG','config2')),(cv2.getTrackbarPos('CHI---epsR','config2'))]
            v1 = cv2.compareHist(histB, histB1, cv2.cv.CV_COMP_CHISQR)
            v2 = cv2.compareHist(histG, histG1, cv2.cv.CV_COMP_CHISQR)
            v3 = cv2.compareHist(histR, histR1, cv2.cv.CV_COMP_CHISQR) 
            v = [v1, v2, v3]

            image = img.copy()
            cv2.putText(image,str(v),(50,img.shape[0]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(100,0,200))

            # if showAllImages!=0 then want show all compare_images
            if showAllImages==2:# shows resize image
                copy_img = cv2.resize(image, (int(img.shape[1]*0.75), int(img.shape[0]*0.75)))
                cv2.imshow(str(im[2]),copy_img)
                j = j+1
            if showAllImages==1:# shows real image
                cv2.imshow(str(im[2]),image)
                j = j+1

            # if a value of v is not lesser epsilon then not keep looking
            for i in range(len(v)):
                if v[i]> eps[i]:
                    break
                elif i == len(v)-1:
                    imToShow = imToShow+[[im[0],image,im[2]]]
                    returnImg = returnImg + [im]

    # shows all selected images
    j = 1
    for im in imToShow:
        if showHist:
            # calculates imToShow histogram and shows it near real image
            img = im[1]
            h = img.shape[0]
            w = img.shape[1]+256
            imhist = np.zeros((h,w,3),np.uint8)
            imhist[:,0:img.shape[1]] = img

            hist = np.zeros((h,256,3));
            b,g,r = img[:,:,0],img[:,:,1],img[:,:,2]
            bins = np.arange(257)
            bin = bins[0:-1]
            color = [ (255,0,0),(0,255,0),(0,0,255) ]
	
            for item,col in zip([b,g,r],color):
		N,bins = np.histogram(item,bins)
		v=N.max()
		N = np.int32(np.around((N*255)/v))
		N=N.reshape(256,1)
		pts = np.column_stack((bin,N))
		cv2.polylines(hist,np.array([pts],np.int32),False,col,2)
                
            hist=np.flipud(hist)
            imhist[:,im[1].shape[1]:] = hist
        
            # shows imhist
            cv2.imshow('selected_'+str(im[2]),imhist)
        else:
            cv2.imshow('selected_'+str(im[2]),im[1])
        if showSelectMask == 1:# show selected image mask
            cv2.imshow('im_mask_'+str(im[2]),im[0])
        j = j+1

    return returnImg

def findMask(images_name):
    # for each image calculates its mask
    print help_message 
    compare_images = []
    for img_name in images_name :
        img = cv2.imread(img_name)
        compare_images = compare_images + [calcBinaryImage2.calcMask(img,img_name)]
    return compare_images

def compareByColor(compareImages): 
    global compare_images, chi, histB,histG, histR, show_hist
    compare_images = []

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
  c    -   change histogram comparison method
  h    -   show histograms

'''                      
    chi = True
    print 'chi square'
    show_hist = True

    # creates config window with its trackbars
    cv2.namedWindow('config2')
    cv2.createTrackbar('CORR---epsB','config2',17,20,dummy)#.7
    cv2.createTrackbar('CORR---epsG','config2',17,20,dummy)
    cv2.createTrackbar('CORR---epsR','config2',17,20,dummy)
    cv2.createTrackbar('CHI---epsB','config2',4,40,dummy)
    cv2.createTrackbar('CHI---epsG','config2',4,40,dummy)
    cv2.createTrackbar('CHI---epsR','config2',4,40,dummy)
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
    returnImg = compareHist(compare_images, histB, histG, histR, chi, show_hist)

    while True:
        cv2.imshow('image',pimg)
        key = cv2.waitKey(5)
        # removes old windows and calculates the most similar images with the new values
        if key == ord('s'):
            for im in compare_images:
                cv2.destroyWindow('im_'+str(im[2]))
                cv2.destroyWindow('im_mask_'+str(im[2]))
                cv2.destroyWindow(str(im[2]))
                cv2.destroyWindow('selected_'+str(im[2]))
            cv2.imshow('image',pimg)
            returnImg = compareHist(compare_images, histB, histG, histR, chi, show_hist)
        if key == ord('c'):
            chi = not chi
            if chi:
                print 'chi square'
            else:
                print 'correlation'
        if key == ord('h'):#shows histograms
            show_hist = not show_hist
            for im in compare_images:
                cv2.destroyWindow('im_'+str(im[2]))
                cv2.destroyWindow('im_mask_'+str(im[2]))
                cv2.destroyWindow(str(im[2]))
                cv2.destroyWindow('selected_'+str(im[2]))
            cv2.imshow('image',pimg)
            returnImg = compareHist(compare_images, histB, histG, histR, chi, show_hist)
            
        # EXIT
        if key == ord('q'):
            cv2.destroyWindow('image')
            cv2.destroyWindow('config2')
            for im in compare_images:
                cv2.destroyWindow('im_'+str(im[2]))
                cv2.destroyWindow('im_mask_'+str(im[2]))
                cv2.destroyWindow(str(im[2]))
                cv2.destroyWindow('selected_'+str(im[2]))
            return returnImg
  
def compare(images_name):
    compare_images = findMask(images_name)
    selectedImages = compareByColor(compare_images)
    return selectedImages

if __name__ == "__main__":

    images_name = sys.argv[1:]

    compare(images_name)
