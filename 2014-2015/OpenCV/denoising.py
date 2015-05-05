import cv2
from matplotlib import pyplot as plt

# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_photo/py_non_local_means/py_non_local_means.html

img = cv2.imread('at4.tif')

dst = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)

plt.subplot(121), plt.imshow(img)
plt.subplot(122), plt.imshow(dst)
plt.show()