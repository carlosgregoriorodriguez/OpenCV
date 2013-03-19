#! /usr/bin/python
# opencv 2.3.1

import cv2
import sys
import numpy as np
import searchBySize_new
import resizeAndWrite
import searchByColor


def dummy(pos):
    if cv2.getTrackbarPos('resize and write','What do you do?')==1:
        for img in name_images:
            resizeAndWrite.resizeAndWrite(cv2.imread(img))
            cv2.waitKey(0)
        cv2.setTrackbarPos('resize and write','What do you do?',0)
        cv2.destroyWindow('image resize')
        cv2.destroyWindow('special images')

    if cv2.getTrackbarPos('search by size','What do you do?')==1:
        searchBySize_new.compareBySize(name_images)
        cv2.destroyAllWindows()
        cv2.namedWindow('What do you do?')
        cv2.createTrackbar('resize and write','What do you do?',0,1,dummy)
        cv2.createTrackbar('search by size','What do you do?',0,1,dummy)
        cv2.createTrackbar('search by color','What do you do?',0,1,dummy)

    if cv2.getTrackbarPos('search by color','What do you do?')==1:
        searchByColor.compareByColor(name_images)
        cv2.destroyAllWindows()
        cv2.namedWindow('What do you do?')
        cv2.createTrackbar('resize and write','What do you do?',0,1,dummy)
        cv2.createTrackbar('search by size','What do you do?',0,1,dummy)
        cv2.createTrackbar('search by color','What do you do?',0,1,dummy)
        
if __name__ == '__main__':
    global name_images
    name_images = sys.argv[1:]
    
    cv2.namedWindow('What do you do?')
    cv2.createTrackbar('resize and write','What do you do?',0,1,dummy)
    cv2.createTrackbar('search by size','What do you do?',0,1,dummy)
    cv2.createTrackbar('search by color','What do you do?',0,1,dummy)
    #cv2.imshow('i',cv2.imread(name_images[0]))
    while True:
        key = cv2.waitKey(20)
        if key == 27:
            break
        
