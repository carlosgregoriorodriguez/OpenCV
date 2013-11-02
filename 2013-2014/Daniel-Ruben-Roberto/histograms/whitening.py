__author__ = 'daniel'
# -*- coding: UTF-8 -*-

import cv2
import numpy as np

#Inicializamos variables
img = cv2.imread("../../img/beach1.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
cv2.imshow("original", img)

I, J = img.shape
media = 0
var = 0

#Calculamos media
for i in range(I):
    for j in range(J):
        media += img[i, j]
media = media/(I*J)

#Calculamos varianza
for i in range(I):
    for j in range(J):
        var += (abs(img[i, j] - media))**2
var = var/(I*J)

#Blanqueamos
vis = np.zeros((I, J), np.float32)
dst = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
for i in range(I):
    for j in range(J):
        dst[i, j] = (abs(img[i, j] - media))/(var**0.5)
cv2.imshow("resultado", dst)
cv2.waitKey(0)