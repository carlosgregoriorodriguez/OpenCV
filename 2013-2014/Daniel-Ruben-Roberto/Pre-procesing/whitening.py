__author__ = 'daniel'
# -*- coding: UTF-8 -*-

import cv2
import numpy as np

#Inicializamos variables
#def whitening(img):
img = cv2.imread("../../img/beach1.jpg", cv2.CV_LOAD_IMAGE_COLOR)
cv2.imshow("original", img)

b, g, r = cv2.split(img)
todos = b, g, r

media = 0
var = 0
dummy = 0
for img in todos:
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
            var += (img[i, j] - media)**2
    var = var/(I*J)

    #Blanqueamos
    vis = np.zeros((I, J), np.float32)
    dst = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
    for i in range(I):
        for j in range(J):
            dst[i, j] = (img[i, j] - media)/(var**0.5)
    assert isinstance(dst, object)
    text = "resultado", "b", "g", "r"
    cv2.imshow(text[0] + text[dummy], dst)
    dummy += 1
cv2.waitKey(0)
#return dst