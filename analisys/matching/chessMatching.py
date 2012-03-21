#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

#TEST Match Template ...

#Usage-   python chessMatching.py ___
#                                   -> big : for BIG chess
#                                   -> anything else (but not blank) for small

import cv2
import numpy as np
import sys

if __name__ == "__main__":

    if (sys.argv[1] == "big"):
        img = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.imread("../../img/chessboard.png",0))))

    else:
        img = cv2.imread("../../img/smallchessboard.jpg",0)

    cv2.imshow("ORIGINAL",img)
    tmp = cv2.imread("../../img/squareTemplate.jpg",0)
    cv2.imshow("TEMPLATE",tmp)

    result1 = cv2.matchTemplate(img,tmp,method=cv2.TM_CCORR)
    cv2.imshow("matchings CCORR",result1)

    result2 = cv2.matchTemplate(img,tmp,method=cv2.TM_SQDIFF)
    cv2.imshow("matchings SQDIFF",result2)

    result3 = cv2.matchTemplate(img,tmp,method=cv2.TM_CCOEFF)
    cv2.imshow("matchings CCOEFF",result3)

    cv2.waitKey(0)
