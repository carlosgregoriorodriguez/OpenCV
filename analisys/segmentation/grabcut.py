import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys

print "Usage:"
print "python grabcut.py --> default image an rectangle"
print "python grubcut.py img x y with legth --> img and rectangle with (x,y) left upper corner and with and length"
print "Example: python grabcut.py foto.jpg 700 300 400 500"

filename = "pills.png"
rect = (100,50,250,300)
if len(sys.argv)>1:
    filename = sys.argv[1]
    rect = tuple([int(x) for x in sys.argv[2:]])
    #foto.jpg 700 300 400 500
im = cv2.imread(filename)

h,w = im.shape[:2]

mask = np.zeros((h,w),dtype='uint8')
tmp1 = np.zeros((1, 13 * 5))
tmp2 = np.zeros((1, 13 * 5))

cv2.grabCut(im,mask,rect,tmp1,tmp2,3,mode=cv2.GC_INIT_WITH_RECT)
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(mask)
#print maxVal, maxLoc
#print mask.dtype
flag, mask = cv2.threshold(mask, maxVal-1, 255, cv2.cv.CV_THRESH_BINARY)
cv2.imshow("mask", mask)

cv2.rectangle(im,(rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),color=255)
cv2.imshow("img+rect",im)


[b,g,r] = cv2.split(im)
cv2.imshow("result", cv2.merge([cv2.min(x,mask) for x in [b,g,r]]))

"""plt.figure()
plt.imshow(mask)
plt.colorbar()
plt.show()
"""
cv2.waitKey(0)
