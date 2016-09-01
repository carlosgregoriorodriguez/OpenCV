import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt

print 'Number of arguments:', len(sys.argv), 'arguments'
print 'Argument List:', str(sys.argv)
if (len(sys.argv)>1):
	imgPath = sys.argv[1]
else:
	imgPath = "imagenTest.jpg"
img = cv2.imread(imgPath,0)
imgCol = cv2.imread(imgPath)
#ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
hist = cv2.calcHist([img],[0],None,[256],[0,256])
ret,thresh = cv2.threshold(img,20,255,0)
#plt.figure(figsize=(2, 2))
plt.subplot(311)
plt.hist(img.ravel(),256,[0,256])
plt.subplot(312)
plt.imshow(thresh)
plt.subplot(313)
plt.imshow(imgCol)
plt.show()