import cv2
import numpy as np

__author__="mimadrid"

imgName = 'edi uveitis previa 11'
img = cv2.imread(imgName+'.png')
windowTitle = 'Imagen'

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

minThres = 0
sobel = img
opening = None
ratio = 3

def fValue(x):
    global sobel
    if x % 2 == 0:
        x -= 1
    sobel = cv2.Sobel(gray,cv2.CV_8U,0,1,ksize=x)
    cv2.imshow(windowTitle, sobel)
   
def ferosionDilate(x):
    global sobel, opening
    if x % 2 == 0:
        x += 1    
    # http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    kernel = np.ones((x,x),np.uint8)
    opening = cv2.morphologyEx(sobel, cv2.MORPH_OPEN, kernel)
    # >> cv2.getStructuringElement(cv2.MORPH_OPEN,(5,5))
    # array([[0, 0, 1, 0, 0],
    #   [1, 1, 1, 1, 1],
    #   [1, 1, 1, 1, 1],
    #   [1, 1, 1, 1, 1],
    #   [0, 0, 1, 0, 0]], dtype=uint8)

    cv2.imshow(windowTitle, opening)
    
def fMinCanny(x):
    global minThres, sobel, ratio, opening
    minThres = x
    if opening is None:
        opening = sobel
    edges =  cv2.Canny(opening,x,x*ratio, apertureSize = 3)
    cv2.imshow(windowTitle, edges)
    
def fRatio(x):
    global ratio, minThres
    ratio = x
    fMinCanny(minThres)

if __name__ == "__main__":
    
    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Kernel size (Scharr = 0)', windowTitle, 0, 31, fValue)
    cv2.createTrackbar('Erosion and the dilate', windowTitle, 5, 31, ferosionDilate)
    cv2.createTrackbar('Canny min', windowTitle, 0, 1000, fMinCanny)
    cv2.createTrackbar('Canny Ratio', windowTitle, 3, 10, fRatio)
 
    cv2.imshow(windowTitle, img)
    while True:

        #key = cv2.waitKey(0)
        # 64 bits
        key = cv2.waitKey(0) & 0xFF
        # 27 = ESC
        if key==27 or key == 113: #ESC or q
            #cv2.destroyAllWindows()
            cv2.destroyWindow(windowTitle)
            #cv2.imwrite(imgName +'.png', img)
            break
