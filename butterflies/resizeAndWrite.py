#! /usr/bin/python
# opencv 2.3.1

import cv2
import sys
import numpy as np
import datetime
import floodfillgray_new

def find_rectangle(contours):
    final_rect = [0,0,0,0]
    rectangles = []
    for contour in contours:
        minrect = cv2.boundingRect(contour)        
        area = minrect[2]*minrect[3]  
        if area < 100800-100 and minrect[2]>minrect[3]*2 and area>10000 and minrect[2]/minrect[3]>2 and minrect[2]/minrect[3]< 4 :
            rectangles = rectangles + [minrect]
            final_rect = minrect
    if (len(rectangles)>1):
        dist = 5
        for i in range(len(rectangles)):
            if (dist > abs(rectangles[i][2]/rectangles[i][3]-3.5)):
                dist = abs(rectangles[i][2]/rectangles[i][3]-3.5)
                final_rect = rectangles[i] 
    return final_rect


def resize(img,final_rect):
        #102 y 349 es el valor medio de w y h, respectivamente, de todas las imagenes en las que detecta qp
        w =  img.shape[0]*(102)/final_rect[3]
        h = img.shape[1]*(349)/final_rect[2]
        imgResize = cv2.resize(img,(h,w), None, 1, 1, cv2.INTER_CUBIC)
        
        return imgResize

def resizeAndWrite(img):
        #search the area where it's more probably to find the qp
        template = cv2.imread('qp.jpg')
        imgfound = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
        minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(imgfound)

        #reduces the image to the area most probably
        reduced_img = np.zeros(img.shape,np.uint8)+255
        reduced_img[minLoc[1]-40:img.shape[0],minLoc[0]-40:img.shape[1]] = img[minLoc[1]-40:img.shape[0],minLoc[0]-40:img.shape[1]]
        imgthres = floodfillgray_new.flooded(reduced_img,27,255,51)

        #computes the contours
        imgcanny = imgthres.copy()
        imgcanny = cv2.Canny(cv2.cvtColor(imgcanny,cv2.cv.CV_RGB2GRAY), 147,600)
        contours, hierarchy = cv2.findContours(imgcanny.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cv2.approxPolyDP(contour, 1, True) for contour in contours];

        #computes the rectangle most similar with the qp card
        final_rect = find_rectangle(contours)      
        cv2.rectangle(img,(final_rect[0],final_rect[1]),(final_rect[2]+final_rect[0],final_rect[3]+final_rect[1]),(0,0,255))

        #resize and write the image
        if final_rect != [0,0,0,0]:
            imgResize = resize(img,final_rect)
            cv2.imshow('image resize',imgResize)
            now = datetime.datetime.now()
            #cv2.imwrite('butterflies_resize/foto'+str(now.day)+str(now.month)+str(now.minute)+str(now.second)+'.jpg',imgResize)
            return imgResize
        else:
            cv2.imshow('special images', img)
            return img
           # cv2.imwrite('butterflies_special/foto'+str(now.day)+str(now.month)+str(now.minute)+str(now.second)+'.jpg',img)



if __name__ == '__main__':

    name_images = sys.argv[1:]
    
    for name in name_images:

        img = cv2.imread(name)
        cv2.imshow('image',img)
        resizeAndWrite(img)
        k = cv2.waitKey(0)


