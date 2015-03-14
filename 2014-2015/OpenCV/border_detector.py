import cv2

__author__="mimadrid"

imgName = 'edi uveitis previa 11 threshold'
img = cv2.imread(imgName+'.png')
windowTitle = 'Imagen'

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

minThres = 0
maxThres = 100
sobel = img
blur = None
ratio = 3

def fValue(x):
    global sobel
    if x % 2 == 0:
        x -= 1
    sobel = cv2.Sobel(gray,cv2.CV_8U,0,1,ksize=x)
    cv2.imshow(windowTitle, sobel)

def fBlur(x):
    global sobel, blur
    if x % 2 == 0:
        x += 1
    blur = cv2.medianBlur(sobel,x)
    #blur = cv2.blur(sobel,(x,x))
    cv2.imshow(windowTitle, blur)
    
def fMinCanny(x):
    global minThres, maxThres, blur, sobel, ratio
    minThres = x
    if blur is None:
        blur = sobel
    edges =  cv2.Canny(blur,x,x*ratio, apertureSize = 3)
    cv2.imshow(windowTitle, edges)
    
def fRatio(x):
    global ratio
    ratio = x    

if __name__ == "__main__":
    
    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Kernel size (Scharr = 0)', windowTitle, 0, 31, fValue)
    cv2.createTrackbar('Blur', windowTitle, 0, 100, fBlur)
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
