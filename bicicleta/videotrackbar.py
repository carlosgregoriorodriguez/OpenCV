#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import sys
import cv2


pos = 0


def show(img):
    p = int(vid.get(cv2.cv.CV_CAP_PROP_POS_MSEC))
    cv2.putText(img,str(p/1000.0),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
    cv2.imshow("ori",img)
    
def onTrackbarSlidePos(pos):
    global vid, img
    vid.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos)
    f,img = vid.read()
    show(img)
    
def process(img):
    cv2.namedWindow("img")
    cv2.imshow("img",img)
    cv2.waitKey(-1)
    cv2.destroyWindow("img")
    
def main():
    global vid
    
    vid = cv2.VideoCapture(sys.argv[1])
    frame_count = int(vid.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    cv2.namedWindow("ori")
    if frame_count != 0:
        cv2.createTrackbar("pos","ori",1,frame_count,onTrackbarSlidePos)

    while True:
        f,img = vid.read()
        show(img)
        k = cv2.waitKey (-1)
        if k==27:
            break
        elif k==ord("p"):
            process(img)
    
if __name__ == "__main__": 
    main()
