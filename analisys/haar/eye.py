# -*- coding: utf-8 -*-
#! /usr/bin/env python
# opencv 2.3.1

import cv2
import cv2.cv as cv #solo para algunas constantes

import sys
import time

def getFrame(camera, grayscale=False, flip=True):    
    f,frame = camera.read()
    while not f:
        print "Lost frame... trying again"
        f,frame = camera.read()
    if flip:
        frame = cv2.flip(frame, 1)
    if grayscale:
        return cv2.cvtColor(frame,cv.CV_RGB2GRAY)
    else:
        return frame

def InputKey(camera): 
    global debug
    QUIT = "q" 
    k = cv2.waitKey (10)
    if (k != -1):
        if (k in range(256)):          
            step = 0.1
            if (chr(k) == QUIT):
                print "Quit"
                exit()
            elif (chr(k) == "1"):
                cb = camera.get(cv.CV_CAP_PROP_BRIGHTNESS)
                if debug :
                    print "-- brightness: ", cb - step
                camera.set(cv.CV_CAP_PROP_BRIGHTNESS, cb - step)
            elif (chr(k) == "2"): 
                cb = camera.get(cv.CV_CAP_PROP_BRIGHTNESS)
                if debug :
                    print "++ brightness ", cb + step
                camera.set(cv.CV_CAP_PROP_BRIGHTNESS, cb + step)
            elif debug:
                print "key", chr(k), "value", k
        else:
            if debug :
                print "key value not valid for chr()", k    
            
if __name__ == "__main__":
    print ""
    debug = True
    camera =  cv2.VideoCapture(0)

    cascade_file = "classifier/eye.xml"

    cascade = cv2.CascadeClassifier(cascade_file)

    while 1:
        img = getFrame(camera,grayscale=False)
        img = cv2.pyrDown(img)

        minSize = (10,10)
        maxSize = (200,200)
        scaleFactor = 1.1
        minNeighbors = 3
        flags = 0

        eyes = cascade.detectMultiScale(img, scaleFactor, minNeighbors, flags, minSize, maxSize)

        for eye_rect in eyes:
            print eye_rect #x_0,y_0,width,height
            cv2.rectangle(img,(eye_rect[0],eye_rect[1]),(eye_rect[0]+eye_rect[2],eye_rect[1]+eye_rect[3]),(255,0,0))            

        cv2.imshow("eyes",img)

        InputKey(camera)        
