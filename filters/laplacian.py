#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

# FILTER TEST : Laplacian
#

import cv2
import numpy
import sys

if __name__ == "__main__":

    img = cv2.imread(sys.argv[1],0)
    cv2.imshow("ORIGINAL",img)
    imgLap = cv2.Laplacian(img,2)
    cv2.imshow("LAPLACIAN",numpy.array(imgLap,dtype="uint8"))

    cv2.waitKey(0)
    
