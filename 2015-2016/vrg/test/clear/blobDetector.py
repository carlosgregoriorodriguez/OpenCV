# Standard imports
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Read image
filename= "placa.jpg"
img = cv2.imread(filename, 0)
img_color = cv2.imread(filename, cv2.IMREAD_ANYCOLOR)
img_c = cv2.resize(img_color,(800,600))
img1 = cv2.resize(img,(800,600))
ret,im = cv2.threshold(img1,120,255,cv2.THRESH_BINARY)

#######################################################
#######################################################

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 50
params.maxThreshold = 150

# Filter by Area.
params.filterByArea = True
params.minArea = 150
params.maxArea = 400

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.2

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.1

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.01

detector = cv2.SimpleBlobDetector_create(params)

#######################################################
#######################################################

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(img_c, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)

x=[]
y=[]
area=[]

for i in xrange(9):
    xx = keypoints[i].pt[0]
    yy = keypoints[i].pt[1]
    aarea = keypoints[i].size
    print "PT.%f -- " %i, "x = %f," %xx, "y = %f," %yy,"area = %f," %aarea, "\n"

#######################################################
#######################################################
cv2.waitKey(0)