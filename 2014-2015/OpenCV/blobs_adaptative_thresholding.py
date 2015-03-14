import cv2
from SimpleCV import Image, Color
__author__="mimadrid"

imgName = 'poros papila'
img = cv2.imread(imgName+'.bmp', 0)
windowTitle = 'Imagen'

maxValue = 255
na = 11
cons = 2;
thres = None
tipo = 0

def fneighbourdhood_area(x):
    global na, thres, windowTitle, tipo
    if x % 2 ==0:
        na = x+1
    else:
        na = x
    if na == 0 or na == 1:
        na = 3
    if tipo == 0:
        thres = img
    elif tipo == 1:
        thres = cv2.adaptiveThreshold(img, maxValue,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, na, cons)
    elif tipo == 2:
        thres = cv2.adaptiveThreshold(img, maxValue, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,na,cons)
    blobImg = Image(thres)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    
    cv2.imshow(windowTitle, thres)

def fConstant(x):
    global cons, thres, windowTitle, tipo, maxValue, na, img
    # const positive to white, otherwise, to black
    cons = x
    if tipo == 0:
        thres = img
    elif tipo == 1:
        thres = cv2.adaptiveThreshold(img, maxValue,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, na, cons)
    elif tipo == 2:
        thres = cv2.adaptiveThreshold(img, maxValue, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,na,cons)
    
    blobImg = Image(thres)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, thres)


def fMaxValue(x):
    global maxValue, windowTitle, thres, img, na, cons
    maxValue = x
    if tipo == 0:
        thres = img
    elif tipo == 1:
        thres = cv2.adaptiveThreshold(img, maxValue,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, na, cons)
    elif tipo == 2:
        thres = cv2.adaptiveThreshold(img, maxValue, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,na,cons)
    
    blobImg = Image(thres)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, thres)

def adaptative_thresholding(x):
    global thres, na, cons, maxValue, tipo, img, windoTitle
    if x == 0:
        thres = img
        maxValue = 255
        na = 11
        cons = 2;
        cv2.createTrackbar('Neighbourhood area (odds)', windowTitle, na, maxValue, fneighbourdhood_area)
        cv2.createTrackbar('Constant', windowTitle, -maxValue, maxValue, fConstant)
        cv2.createTrackbar('MaxValue', windowTitle, maxValue, maxValue, fMaxValue)
    elif x == 1:
        thres = cv2.adaptiveThreshold(img, maxValue,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, na, cons)
    elif x == 2:
        thres = cv2.adaptiveThreshold(img, maxValue, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,na,cons)
    tipo = x
    blobImg = Image(thres)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, thres)

if __name__ == "__main__":
    # 0 = cv2.IMREAD_GRAYSCALE
    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)

    cv2.createTrackbar('Neighbourhood area (odds)', windowTitle, na, maxValue, fneighbourdhood_area)
    cv2.createTrackbar('Constant', windowTitle, cons, maxValue, fConstant)
    cv2.createTrackbar('MaxValue', windowTitle, maxValue, maxValue, fMaxValue)
    cv2.createTrackbar('NORMAL\nAdaptive Gaussian Thresholding\nAdaptive Mean Thresholding', windowTitle,0, 2, adaptative_thresholding)

    cv2.imshow(windowTitle, img)
    while True:

        #key = cv2.waitKey(0)
        # 64 bits
        key = cv2.waitKey(0) & 0xFF
        # 27 = ESC
        if key==27:
            #cv2.destroyAllWindows()
            cv2.destroyWindow(windowTitle)
            #cv2.imwrite(imgName +'.png', img)
            break
