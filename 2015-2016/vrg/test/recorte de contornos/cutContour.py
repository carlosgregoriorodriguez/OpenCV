#recorte de contornos
import numpy as np
import cv2

radius = 20

gray = cv2.imread("testRecorte.png",0)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
cv2.circle(gray, maxLoc, radius, (0, 0, 0), 2)
cv2.imshow("Original",gray)
cv2.waitKey(0)

gray = cv2.imread("testRecorte.png",0)
blur = cv2.blur(gray, (radius,radius), 5)
cv2.imshow("blur",blur)
cv2.waitKey(0)

(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)
print maxLoc
cv2.circle(gray, maxLoc, radius, (0, 0, 0), 2)

cv2.imshow('image',gray)
cv2.waitKey(0)
cv2.destroyAllWindows()