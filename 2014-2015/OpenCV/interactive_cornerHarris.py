import cv2
import numpy as np

# Credentials to http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html

filename = 'edi uveitis final6.png'
windowTitle = 'corner_harris'
img = cv2.imread(filename)

blockSize_value = 2 
ksize_value = 3
k_value = 0.15
thresh = 0.01

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
# img - Input image, it should be grayscale and float32 type.
# blockSize - It is the size of neighbourhood considered for corner detection
# ksize - Aperture parameter of Sobel derivative used.
# k - Harris detector free parameter in the equation.
#dst = cv2.cornerHarris(gray, 2, 3, 0.15)

#result is dilated for marking the corners, not important
#dst = cv2.dilate(dst, None)

# Threshold for an optimal value, it may vary depending on the image.
#img[dst > 0.01 * dst.max()] = [0, 0, 255]

#cv2.imshow('dst', img)

def showImg ():
    global gray, blockSize_value, ksize_value, k_value, filename
    #print ("blockSize_value %s \n ksize_value = %s \n k_value = %s \n" % (blockSize_value, ksize_value, k_value)) 
    harris = cv2.cornerHarris(gray, blockSize_value, ksize_value, k_value)
    harris = cv2.dilate(harris, None)
    result = cv2.imread(filename)
    result[harris > thresh * harris.max()] = [0, 0, 255]
    cv2.imshow(windowTitle, result)


def blockSize(value):
    global blockSize_value
    if value == 0:
        value += 1
    blockSize_value = value    
    showImg()
    
def ksize(value):
    global ksize_value
    if value % 2 == 0:
        value += 1
    ksize_value = value
    showImg()

def k(value):
    global k_value
    k_value = value /100.0
    showImg()
    
def threslhold(value):
    global thresh
    thresh = value /100.0
    showImg()
    

if __name__ == "__main__":

    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('blockSize', windowTitle, 2, 100, blockSize)
    cv2.createTrackbar('ksize', windowTitle, 3, 29, ksize)
    cv2.createTrackbar('k', windowTitle, 15, 100, k)
    cv2.createTrackbar('threshold', windowTitle, 1, 100, threslhold)
    showImg()
    
    while True:
        # 0xFF para 64 bits
        key = cv2.waitKey(0) & 0xFF
        # 27 = ESC 113 = q
        if key == 27 or key == 113:
            break
       
    cv2.destroyWindow(windowTitle)