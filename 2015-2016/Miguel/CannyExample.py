import cv2
import sys

def nada(x):
    pass
img = cv2.imread("1.png", 0)


cv2.namedWindow('canny',cv2.WINDOW_NORMAL)

switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'canny', 0, 1, nada)
cv2.createTrackbar('lower', 'canny', 0, 255, nada)
cv2.createTrackbar('upper', 'canny', 0, 255, nada)

while(True):
    lower = cv2.getTrackbarPos('lower', 'canny')
    upper = cv2.getTrackbarPos('upper', 'canny')
    s = cv2.getTrackbarPos(switch, 'canny')

    if s == 0:
        edges = img
    else:
        edges = cv2.Canny(img, lower, upper)

    cv2.imshow('original', img)
    cv2.imshow('canny', edges)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
