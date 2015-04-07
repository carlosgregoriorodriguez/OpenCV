import cv2
from matplotlib import pyplot as plt

img = cv2.imread('poros papila.bmp', 0)

# Initiate STAR detector
orb = cv2.ORB()

ret, otsu_threshold = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# find the keypoints with ORB
kp = orb.detect(otsu_threshold, None)

# compute the descriptors with ORB
kp, des = orb.compute(otsu_threshold, kp)

# draw only keypoints location,not size and orientation
img2 = cv2.drawKeypoints(img, kp, color=(0, 255, 0), flags=0)
plt.imshow(img2), plt.show()