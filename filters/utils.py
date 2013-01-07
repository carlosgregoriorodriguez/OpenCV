# -*- coding: utf-8 -*-
#! /usr/bin/env python
# opencv 2.3.1

import sys
import time
import cv2.cv as cv #solo para algunas constantes
import cv2
import numpy as np
from parameters import parameters

def dummy(v):
    global debug
    if debug :
        print "modified value:", v

def createTestFrame(window_name, parameters):
    cv2.namedWindow(window_name)
    for k, v in parameters.iteritems():
        if len(v) > 2:
            cv2.createTrackbar(k+v[2].func_name,window_name,v[0],v[1],dummy)
        else:
            cv2.createTrackbar(k, window_name,v[0],v[1],dummy)

def test(window_name, img_in, f, parameters, speed=True):      
    func_param = {}
    for k in iter(parameters):
        if len(parameters[k]) > 2:
            func_param[k] = parameters[k][2](cv2.getTrackbarPos(k+parameters[k][2].func_name,window_name))
        else:
            func_param[k] = cv2.getTrackbarPos(k,window_name) 
    before = time.time()
    img_out = apply(f,(img_in,),func_param)
    if speed :
        fps = 1/(time.time()-before)
        cv2.putText(img=img_out, text=str(fps)+" fps", org=(50, 50), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                    color=(0, 0, 0), thickness = 2, linetype=cv2.CV_AA)        
    cv2.imshow(window_name, img_out)
    return img_out

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

def InputKey(camera, pause=False):
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
            elif (chr(k) == "p"):
                pause = not pause
                print "Pause", pause
            elif debug:
                print "key", chr(k), "value", k
        else:
            if debug :
                print "key value not valid for chr()", k    
    return pause        
if __name__ == "__main__":
    print "Sample code for using utils mini module"
    debug = False
    pause = False
              
    camera =  cv2.VideoCapture(0)
        
    func_names = ['erode','dilate','Canny']
    
    for name in func_names:
        createTestFrame(name,parameters[name])
    while 1:
        if not pause:
            img = getFrame(camera,grayscale=True)
        cv2.imshow("original",img)
        for name in func_names:
            test(name,img,eval("cv2."+name),parameters[name])
        pause = InputKey(camera, pause)        
