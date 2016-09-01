#valido para detectar estrellas con lensflare, ver caso del contorno 358 para imagenTest.jpg
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('imagenTest.jpg',0)
ret,thresh = cv2.threshold(img,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#http://docs.opencv.org/trunk/d4/d73/tutorial_py_contours_begin.html#gsc.tab=0
print "Num de candidatos: "+str(len(contours))
#cv2.drawContours(img, contours, -1, (0,255,0), 3)
miContorno = 358
cv2.drawContours(img, contours, miContorno, (0,255,0), 10)
cnt = contours[miContorno]
#cv2.drawContours(img, [cnt], 0, (0,255,0), 3)
print contours[miContorno]
#cv2.drawContours(img, contours[5], 0, (0,0,0), 80)
#cv2.drawContours(img, contours[320], 0, (255,255,255), 80)
#print contours
plt.imshow(img)
plt.show()
print "Finished"
	