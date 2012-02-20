#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
          
if __name__ == "__main__":

    img = cv2.imread(sys.argv[1])
    cv2.imshow("img",img)    
    cv2.waitKey (0)
