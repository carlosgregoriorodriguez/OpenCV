import numpy as np
import cv2
from matplotlib import pyplot as plt

# Credentials to http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_shi_tomasi/py_shi_tomasi.html

img = cv2.imread('canny_simplecv_11.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# image - Input 8-bit or floating-point 32-bit, single-channel image.
# maxCorners - Maximum number of corners to return. If there are more corners than are found, the strongest of them is returned.
# qualityLevel - Parameter characterizing the minimal accepted quality of image corners. 
# parameter value is multiplied by the best corner quality measure, which is the minimal eigenvalue (see cornerMinEigenVal() ) or the Harris function response (see cornerHarris() ).
# The corners with the quality measure less than the product are rejected. 
# For example, if the best corner has the quality measure = 1500, and the qualityLevel=0.01 , then all the corners with the quality measure less than 15 are rejected.
# minDistance - Minimum possible Euclidean distance between the returned corners.
corners = cv2.goodFeaturesToTrack(gray,25,0.5,10)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,255,-1)

plt.imshow(img),plt.show()


