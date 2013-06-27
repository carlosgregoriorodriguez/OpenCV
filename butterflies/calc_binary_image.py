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
  ESC  -   moves to the next image for analyzing without save the binary image

'''

def onMouse(event, x, y, flag, param):
    global seed_pt
    if flag & cv2.EVENT_FLAG_LBUTTON:
        seed_pt = x, y
        on_flooding_trackbar()



def flooding(img):
    # modifies copy_isolated_butt
    global copy_isolated_butt, new_flood
    # if new_flood is true, update the floodFill image (removes previous floodFills) and make the basics floodFills in the new image. If new_flood is false make the floodFills on img
    if new_flood:
        img = img_contours.copy()
        new_flood = False
        # floodFill on the img underside
        cv2.floodFill(img, mask, (128,copy_isolated_butt.shape[0]-5), (255, 255, 255), (3,)*3, (60,)*3, flags = 4)
        cv2.floodFill(img, mask, (11,copy_isolated_butt.shape[0]-6), (255, 255, 255), (2,)*3, (100,)*3) 
        cv2.floodFill(img, mask, (copy_isolated_butt.shape[1]-1,copy_isolated_butt.shape[0]-1), (255, 255, 255), (2,)*3, (70,)*3)
        # floodFill on the left side of img
        cv2.floodFill(img, mask, (1,10), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
        cv2.floodFill(img, mask, (1,copy_isolated_butt.shape[0]-1), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
        #cv2.floodFill(img, mask, (15,copy_isolated_butt.shape[0]-38), (255, 255, 255), (2,)*3, (60,)*3, flags=4)
        # floodFill on uper right corner of img
        cv2.floodFill(img, mask, (copy_isolated_butt.shape[1]-3,3), (255,255,255), (2,)*3, (60,)*3)
              
    flags = connectivity
    if fixed_range:
        flags |= cv2.FLOODFILL_FIXED_RANGE
    if seed_pt != None:
        lo = cv2.getTrackbarPos('floodfill_lo','config')
        hi = cv2.getTrackbarPos('floodfill_hi','config')
        cv2.floodFill(img, None, seed_pt, (255, 255, 255), (lo,)*3, (hi,)*3)
    cv2.imshow('floodfill',img)
    # update copy_isolated_img with new changes
    copy_isolated_butt = img.copy()
    return img



def filtering(img_butt):
    global img_filter
    # median blur on img_butt
    mb = cv2.getTrackbarPos('medianBlur','config')
    if (mb%2 != 0):
        img = cv2.medianBlur(img_butt,mb)
    else:
        img = cv2.medianBlur(img_butt,mb-1)
    if cv2.getTrackbarPos('debug','config') >= 5:
        cv2.imshow('median_blur',img)
    # erode on median blur image
    img_filter = cv2.erode(img, kernel=None, iterations = cv2.getTrackbarPos('erode','config'))
    if cv2.getTrackbarPos('debug','config') >= 3:
        cv2.imshow('erode',img_filter)
    return img_filter



def calcContours(image):
    global mask
    # transform image to gray scale for calculate edges
    imgbn = cv2.cvtColor(image,cv2.cv.CV_BGR2GRAY)
    # calculate edges with Canny
    canny = cv2.Canny(imgbn,cv2.getTrackbarPos('canny_hi','config'),cv2.getTrackbarPos('canny_lo','config'))
    if cv2.getTrackbarPos('debug','config') >= 4:
        cv2.imshow('canny',canny)
    # initializing mask with canny for use it in floodFill
    mask = np.zeros((canny.shape[0]+2, canny.shape[1]+2), np.uint8)
    mask[1:mask.shape[0]-1, 1:mask.shape[1]-1] = canny
    rawcontours,hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);
    # draw contours on original isolated_img for later floodFill
    imred = isolated_butt.copy()
    cv2.drawContours(imred, rawcontours, -1, (255,0,0), 1, cv2.CV_AA)
    return imred



def thresh(img):
    # modifies final_mask
    global final_mask
    # transform img to gray scale
    imgbn = cv2.cvtColor(img,cv2.cv.CV_BGR2GRAY)
    # threshold imgbn for obtain final binary image
    retVal,img_thres = cv2.threshold(imgbn,254,255,cv2.THRESH_BINARY_INV)
    # erode img_thres
    img_thres = cv2.erode(img_thres, kernel=None, iterations = cv2.getTrackbarPos('erode_mask','config'))
    # copy img_tresh in a black image with the same shape that principal image and on the correct place
    final_mask = np.zeros((shape_image[0],shape_image[1]),np.uint8)
    final_mask[0:point[1]-5,point[0]+10:] = img_thres
    if cv2.getTrackbarPos('debug','config') >= 1:
        cv2.imshow('final_img', final_mask)
    return final_mask



def prepare_image(pos = None):
    global img_contours
    # blur and erode
    img_filter = filtering(isolated_butt)
    # contours
    img_contours = calcContours(img_filter)
    # floodfill
    img_flood = flooding(img_contours)# modifies copy_isolated_butt
    cv2.imshow('floodfill',img_flood)
    # threshold
    img_thres = thresh(img_flood)# modifies final_mask    
    return img_thres



def on_filter_trackbar(pos=None):
    global new_flood
    # destroy old windows
    cv2.destroyWindow('median_blur')
    cv2.destroyWindow('final_img')
    cv2.destroyWindow('erode')
    cv2.destroyWindow('img')
    cv2.destroyWindow('canny')
    new_flood = True
    # calculate all again
    prepare_image()



def on_contour_trackbar(pos=None):
    global img_contours, new_flood
    new_flood = True
    # calculate contours
    img_contours = calcContours(img_filter)
    # floodfill
    img_flood = flooding(copy_isolated_butt)# modifies copy_isolated_butt
    # threshold
    thresh(img_flood)# modifies final_mask



def on_flooding_trackbar(pos=None):
    # floodfill
    img_flood = flooding(copy_isolated_butt)# modifies copy_isolated_butt
    # threshold
    thresh(copy_isolated_butt)# modifies final_mask
    



def calcMask(img, img_name): 
    global compare_images, new_flood, img_contours, seed_pt, copy_isolated_butt, isolated_butt, mask, point, connectivity, fixed_range, final_mask, shape_image
    
    # initializes some data
    connectivity = 4
    seed_pt = None
    fixed_range = True
    mask = []
    shape_image = img.shape
    new_flood = True
    
    # finds the most probable point where is qp
    template = cv2.imread('qp.jpg')
    imgfound = cv2.matchTemplate(img,template, cv2.TM_SQDIFF_NORMED)
    minV,maxV,minL,maxL = cv2.minMaxLoc(imgfound)
    point = (minL[0], minL[1]-35)# less 35 for avoid rule numbers

    # calculate isolated butterfly image using point.
    # use isolated butterfly image and a copy to make changes on the copy (copy_isolated_butt) and keep the other (isolated_butt) such the beginning
    isolated_butt = img[0:point[1]-5, point[0]+10:]# less 5 and more 10 for avoid remains of vertical and horizontal rules
    copy_isolated_butt = isolated_butt.copy()
    
    # initializes img_filter, img_contours and mask 
    img_filter = isolated_butt.copy()
    img_contours = isolated_butt.copy()
    mask = np.zeros((isolated_butt.shape[0]+2, isolated_butt.shape[1]+2), np.uint8)
    
    # creates config window and its trackbars
    cv2.destroyWindow('config')
    cv2.namedWindow('config')
    cv2.namedWindow('floodfill')
    cv2.createTrackbar('debug','config',0,5,on_filter_trackbar)
    cv2.createTrackbar('floodfill_hi','config',60,255,on_flooding_trackbar)
    cv2.createTrackbar('floodfill_lo','config',10,255,on_flooding_trackbar)
    cv2.createTrackbar('canny_hi','config',144,600,on_contour_trackbar)
    cv2.createTrackbar('canny_lo','config',67,600,on_contour_trackbar)
    cv2.createTrackbar('medianBlur','config',2,15,on_filter_trackbar)
    cv2.createTrackbar('erode','config',3,10,on_filter_trackbar)
    cv2.createTrackbar('erode_mask','config',1,10,on_filter_trackbar)
    cv2.setMouseCallback('floodfill',onMouse)

    # calculates the final binary image
    final_mask = prepare_image()


    while True:
        if cv2.getTrackbarPos('debug','config') >= 2:
            cv2.imshow('img',img)
        if cv2.getTrackbarPos('debug','config') >= 1:
            cv2.imshow('final_img',final_mask)
        key = cv2.waitKey(15)
        # save final mask and destroy old windows
        if key == ord('g'):
            cv2.destroyWindow('median_blur')
            cv2.destroyWindow('final_img')
            cv2.destroyWindow('erode')
            cv2.destroyWindow('img')
            cv2.destroyWindow('canny')
            return [final_mask,img,img_name]
        if key == ord('f'):
            fixed_range = not fixed_range
        if key == ord('c'):
            connectivity = 12-connectivity
        # calculates all again with chosen values
        if key == ord('k'):
            new_flood = True
            seed_pt = None
            prepare_image()
        # destroy old windows and exit without save final_mask
        if key == 27:
            cv2.destroyWindow('median_blur')
            cv2.destroyWindow('final_img')
            cv2.destroyWindow('erode')
            cv2.destroyWindow('img')
            cv2.destroyWindow('canny')
            break
    
    



if __name__ == "__main__":
    print help_message

    images_name = sys.argv[1:]# butterflies_resize
    binary_images = []



    for img_name in images_name :

        img = cv2.imread(img_name)
        print 'name ', img_name
        binary_images = binary_images + [calcMask(img,img_name)]
        
        

