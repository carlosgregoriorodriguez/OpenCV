#recorte de contornos
import numpy as np
import cv2

gray = cv2.imread("testRecorte.png",0)
radius = 10
blur = cv2.blur(gray, (10,10), 5)
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
print maxLoc
cv2.circle(blur, maxLoc, radius, (0, 0, 0), -1)

cv2.imshow('image',blur)
cv2.waitKey(0)
cv2.destroyAllWindows()