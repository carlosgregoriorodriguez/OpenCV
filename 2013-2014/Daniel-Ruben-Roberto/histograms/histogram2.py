__author__ = 'daniel'
# -*- coding: UTF-8 -*-
import cv2
import numpy as np

img = cv2.imread("../../img/beach1.jpg", 0)
equ = cv2.equalizeHist(img)
res = np.hstack((img,equ))
cv2.imshow("Resultado", res)
cv2.waitKey(0)
