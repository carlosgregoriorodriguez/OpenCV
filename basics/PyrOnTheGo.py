#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

# Very similar to test_pyrs, but user can modify be pressing keys:
#
#   PRESS 'w' to PyrUp
#         's' to PyrDown
#         'd' to restart Pyr's
#         'e' to capture new image
#
#   PRESS 'r' to change from video captions to the beach image
#
#   PRESS 'q' to QUIT
#
#NOTE: does not work with the video, but with captions.

import cv2

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    f,imgOriginal = camera.read()        
    img = imgOriginal
    
    while True:
     

        k = cv2.waitKey(5)
     
        if (k == 119):      #if user presses 'w' => PyrUp
            img = cv2.pyrUp(img)

        if (k == 115):      #if user presses 's' => PyrDown
            img = cv2.pyrDown(img)

        if (k == 100):      #if user presses 'd' => Restart Pyr's
            img = imgOriginal

        if (k == 101):      #if user presses 'e' => Reset image
            f,imgOriginal = camera.read()
            img = imgOriginal

        if (k == 114):      #if user presser 'r' => Change source (cam ->img)
            imgOriginal = cv2.imread("../img/beach.jpg",2)
            img = imgOriginal

        if (k == 113):      #if user presses 'q' => QUIT
            print "Quit"
            break

    
        cv2.imshow("ORIGINAL",imgOriginal)        

        cv2.imshow("Pyr ON-THE-GO",img)
