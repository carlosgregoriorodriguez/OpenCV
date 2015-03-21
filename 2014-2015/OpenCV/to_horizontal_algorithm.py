import cv2
import numpy as np

__author__ = 'mimadrid'

im = cv2.imread('edi uveitis previa 11.png', 0)
result = None
#gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(im, 150, 200, apertureSize=3)

windowTitle = "horizontal"
cv2.imshow(windowTitle, im)


img = im.copy()
lines = cv2.HoughLines(edges, 1, np.pi / 180, 275)
# http://homepages.inf.ed.ac.uk/rbf/HIPR2/hough.htm
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
# https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/houghlines.py
for rho, theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))   # Here i have used int() instead of rounding the decimal value, so 3.8 --> 3
    y1 = int(y0 + 1000 * (a))    # But if you want to round the number, then use np.around() function, then 3.8 --> 4.0
    x2 = int(x0 - 1000 * (-b))   # But we need integers, so use int() function after that, ie int(np.around(x))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 5)
    
    
    # Use the first not horizontal line as reference and rotate with that theta
    
    # radians to degrees (precision floar error allowed < 1)
    if abs((theta * 180 / np.pi) - 90) > 1: # 90 degrees line is horizontal, not use as reference
        # print "theta = %s\n" % (theta * 180 / np.pi)
        # http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
        rows, cols = im.shape
        # rotate image to the horizontal (line of reference degrees minus 90 degrees)
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), (theta * 180 / np.pi) - 90, 1)
        result = cv2.warpAffine(im, M, (cols, rows))
        break
if result is not None: # rotated image
    cv2.imshow(windowTitle, result)
else:  # Already horizontal image not rotate
    cv2.imshow(windowTitle, img)
    
cv2.waitKey(0) & 0xFF #  64 bits

cv2.destroyAllWindows()