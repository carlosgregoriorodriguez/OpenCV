__author__ = 'daniel'
# -*- coding: UTF-8 -*-
import cv2 as cv
import numpy as np
import sys

if len(sys.argv) == 2:
    im = cv.imread(sys.argv[1])
else:
    im = cv.imread("../../img/beach1.jpg")

h = np.zeros((300, 256, 3))
b, g, r = cv.split(im)
bins = np.arange(256).reshape(256, 1)
color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

for item, col in zip([b, g, r], color):
    hist_item = cv.calcHist([item], [0], None, [256], [0, 255])
    cv.normalize(hist_item, hist_item, 0, 255, cv.NORM_MINMAX)
    hist = np.int32(np.around(hist_item))
    pts = np.column_stack((bins, hist))
    cv.polylines(h, [pts], False, col)

h = np.flipud(h)

cv.imshow('colorhist', h)
cv.waitKey(0)