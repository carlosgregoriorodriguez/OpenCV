#! /usr/bin/python
# opencv 2.3.1

import cv2
import sys
import numpy as np
import searchByColor
import searchBySize_contour

def dummy(pos):
    returnImg = []
    if cv2.getTrackbarPos('color and size','select...') == 1:
        print 'hay '+str(len(name_images))+' imagenes'
        images = searchByColor.compare(name_images)
        print 'han sido seleccionadas por el color ',len(images)
        returnImg = searchBySize_contour.compareBySize(images)
        print 'finalmente quedan ',len(returnImg)
        cv2.setTrackbarPos('color and size','select...',0)
    if cv2.getTrackbarPos('size and color','select...') == 1:
        print 'hay '+str(len(name_images))+' imagenes'
        images = searchBySize_contour.compare(name_images)
        print 'han sido seleccionadas por la forma ',len(images)
        returnImg = searchByColor.compareByColor(images)
        cv2.setTrackbarPos('size and color','select...',0)
        print 'finalmente quedan ',len(returnImg)
    return returnImg
        
    
if __name__ == '__main__':
    global name_images
    name_images = sys.argv[1:]

    cv2.namedWindow('select...')
    cv2.createTrackbar('color and size','select...',0,1,dummy)
    cv2.createTrackbar('size and color','select...',0,1,dummy)

    while True:
        key = cv2.waitKey(20)
        if key == 27:
            break
        
