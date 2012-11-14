#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import sys
import cv2


pos = 0

def onTrackbarSlide(pos):
    vid.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos)

if __name__ == "__main__": 
    
    vid = cv2.VideoCapture(sys.argv[1])
    cv2.namedWindow("video")
    frame = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    
    if frame != 0:
        cv2.createTrackbar("slide","video",1,frame,onTrackbarSlide)

    while True:
        f,img = vid.read()

        p = int(vid.get(cv2.cv.CV_CAP_PROP_POS_MSEC))
        cv2.putText(img,str(p/1000.0),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))

        cv2.imshow("video",img)
       
        # cv2.setTrackbarPos("slide","video",p);

        if (cv2.waitKey (45) != -1):
            break
