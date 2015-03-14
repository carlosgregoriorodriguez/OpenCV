import cv2
from SimpleCV import Image, Color
__author__="mimadrid"

imgName = 'poros papila'
img = cv2.imread(imgName+'.bmp', 0)
windowTitle = 'Imagen'
#windowThres = 'Thresholding'
windowThres = windowTitle

drawing = False
mode = True
ix, iy = -1, -1
value = 127
maxValue = 255
thres = cv2.THRESH_BINARY
filtro = img

maxValueAdaptative = 255
naAdaptative = 11
consAdaptative = 2;
thresAdaptative = None
tipoAdaptative = 0

def fValue(x):
    global value, maxValue, thres, img, filtro
    value = x
    if (thres is None):
        filtro = img

    else:
        ret, filtro = cv2.threshold(img,value, maxValue, thres)
    blobImg = Image(filtro)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, filtro)

def fMaxValue(x):
    global maxValue, value, thres, img, filtro
    maxValue = x
    if (thres is None):
        filtro = img

    else:
        ret, filtro = cv2.threshold(img,value, maxValue, thres)
    blobImg = Image(filtro)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, filtro)

def thresholding(x):
    global thres, value, maxValue, img, filtro
    if (x == 0):
        thres = None
        filtro = img
        value = 127
        maxValue = 255
        cv2.createTrackbar('Value', windowThres, value, maxValue, fValue)
        cv2.createTrackbar('MaxValue', windowThres, maxValue, maxValue, fMaxValue)

    elif (x == 1):
        thres = cv2.THRESH_BINARY
    elif (x==2):
        thres = cv2.THRESH_BINARY_INV

    elif (x==3):
        thres = cv2.THRESH_TRUNC

    elif (x==4):
        thres = cv2.THRESH_TOZERO

    elif (x==5):
        thres = cv2.THRESH_TOZERO_INV
    if (x != 0):
        ret, filtro = cv2.threshold(img,value, maxValue, thres)
    blobImg = Image(filtro)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, filtro)

def fneighbourdhood_area(x):
    global naAdaptative, thresAdaptative, windowTitle, tipoAdaptative, filtro
    if x % 2 ==0:
        naAdaptative = x+1
    else:
        naAdaptative = x
    if naAdaptative == 0 or naAdaptative == 1:
        naAdaptative = 3
    if tipoAdaptative == 0:
        thresAdaptative = img
    elif tipoAdaptative == 1:
        thresAdaptative = cv2.adaptiveThreshold(filtro, maxValueAdaptative,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, naAdaptative, consAdaptative)
    elif tipoAdaptative == 2:
        thresAdaptative = cv2.adaptiveThreshold(filtro, maxValueAdaptative, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,naAdaptative,consAdaptative)
    blobImg = Image(thresAdaptative)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, thresAdaptative)

def fConstant(x):
    global consAdaptative, thresAdaptative, windowTitle, tipoAdaptative, maxValueAdaptative, naAdaptative, img, filtro
    # consAdaptativet positive to white, otherwise, to black
    consAdaptative = x
    if tipoAdaptative == 0:
        thresAdaptative = img
    elif tipoAdaptative == 1:
        thresAdaptative = cv2.adaptiveThreshold(filtro, maxValueAdaptative,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, naAdaptative, consAdaptative)
    elif tipoAdaptative == 2:
        thresAdaptative = cv2.adaptiveThreshold(filtro, maxValueAdaptative, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,naAdaptative,consAdaptative)
    blobImg = Image(thresAdaptative)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, thresAdaptative)


def fMaxValue(x):
    global maxValueAdaptative, windowTitle, thresAdaptative, img, naAdaptative, consAdaptative, filtro
    maxValueAdaptative = x
    if tipoAdaptative == 0:
        thresAdaptative = img
    elif tipoAdaptative == 1:
        thresAdaptative = cv2.adaptiveThreshold(filtro, maxValueAdaptative,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, naAdaptative, consAdaptative)
    elif tipoAdaptative == 2:
        thresAdaptative = cv2.adaptiveThreshold(filtro, maxValueAdaptative, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,naAdaptative,consAdaptative)
    blobImg = Image(thresAdaptative)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, thresAdaptative)

def adaptative_thresAdaptativeholding(x):
    global thresAdaptative, naAdaptative, consAdaptative, maxValueAdaptative, tipoAdaptative, filtro
    if x == 0:
        thresAdaptative = img
        maxValueAdaptative = 255
        naAdaptative = 11
        consAdaptative = 2;
        cv2.createTrackbar('Neighbourhood area (odds)', windowTitle, naAdaptative, maxValueAdaptative, fneighbourdhood_area)
        cv2.createTrackbar('Constant', windowTitle, -maxValueAdaptative, maxValueAdaptative, fConstant)
        cv2.createTrackbar('MaxValue', windowTitle, maxValueAdaptative, maxValueAdaptative, fMaxValue)
    elif x == 1:
        thresAdaptative = cv2.adaptiveThreshold(filtro, maxValueAdaptative,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, naAdaptative, consAdaptative)
    elif x == 2:
        thresAdaptative = cv2.adaptiveThreshold(filtro, maxValueAdaptative, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,naAdaptative,consAdaptative)
    tipoAdaptative = x
    blobImg = Image(thresAdaptative)
    invImg = blobImg.invert()
    blobImg = blobImg.rotate90()
    invImg = blobImg.invert()
    blobs = invImg.findBlobs()
    for blob in blobs:
        #print blob.coordinates()
        invImg.dl().circle(blob.coordinates(), 3, Color.RED, filled = True)
    blobImg.addDrawingLayer(invImg.dl())
    blobs.show(color=Color.GREEN,width=1)
    cv2.imshow(windowTitle, thresAdaptative)

if __name__ == "__main__":
    # 0 = cv2.IMREAD_GRAYSCALE
    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Value', windowThres, value, maxValue, fValue)
    cv2.createTrackbar('MaxValue', windowThres, maxValue, maxValue, fMaxValue)

    cv2.createTrackbar('NORMAL\nTHRESH_BINARY\nTHRESH_BINARY_INV\nTHRESH_TRUNC\nTHRESH_TOZERO\nTHRESH_TOZERO_INV\n', windowThres,0, 5, thresholding)
    cv2.createTrackbar('Neighbourhood area (odds)', windowTitle, naAdaptative, maxValueAdaptative, fneighbourdhood_area)
    cv2.createTrackbar('Constant', windowTitle, consAdaptative, maxValueAdaptative, fConstant)
    cv2.createTrackbar('MaxValue', windowTitle, maxValueAdaptative, maxValueAdaptative, fMaxValue)
    cv2.createTrackbar('NORMAL\nAdaptive Gaussian Thresholding\nAdaptive Mean Thresholding', windowTitle,0, 2, adaptative_thresAdaptativeholding)

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
