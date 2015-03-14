import cv2

__author__="mimadrid"

drawing = False
mode = True
ix, iy = -1, -1
imgName = 'edi uveitis previa 11'
img = cv2.imread(imgName+'.png', 0)
windowTitle = 'Imagen'

value = 0
maxValue = 255
thres = cv2.THRESH_BINARY
tipo = 0

def fValue(x):
    global value, maxValue, thres, img, tipo
    value = x
    imgO = img
    if tipo == 2:
        img  = cv2.GaussianBlur(img,(5,5),0)

    if (thres is None):
        filtro = img
    else:
        ret, filtro = cv2.threshold(img,value, maxValue, thres)
    img = imgO
    cv2.imshow(windowTitle, filtro)

def fMaxValue(x):
    global maxValue, value, thres, img, tipo
    maxValue = x
    imgO = img
    if tipo == 2:
        img  = cv2.GaussianBlur(img,(5,5),0)

    if (thres is None):
        filtro = img

    else:
        ret, filtro = cv2.threshold(img,value, maxValue, thres)
    img = imgO
    cv2.imshow(windowTitle, filtro)

def thresholding(x):
    global thres, value, maxValue, img, tipo
    imgO = img
    if (x == 0):
        thres = None
        filtro = img
        value = 0
        maxValue = 255
        cv2.createTrackbar('Value', windowTitle, value, maxValue, fValue)
        cv2.createTrackbar('MaxValue', windowTitle, maxValue, maxValue, fMaxValue)


    elif (x == 1):
        thres = cv2.THRESH_BINARY+cv2.THRESH_OTSU
    elif (x==2):
        thres = cv2.THRESH_BINARY+cv2.THRESH_OTSU
        img  = cv2.GaussianBlur(img,(5,5),0)
    if (x != 0):
        ret, filtro = cv2.threshold(img,value, maxValue, thres)
    tipo = x
    img = imgO
    cv2.imshow(windowTitle, filtro)

if __name__ == "__main__":
    # 0 = cv2.IMREAD_GRAYSCALE
    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Value', windowTitle, value, maxValue, fValue)
    cv2.createTrackbar('MaxValue', windowTitle, maxValue, maxValue, fMaxValue)

    cv2.createTrackbar("NORMAL\nOtsu's Thresholding\nOtsu's Thresholding\n", windowTitle,0, 2, thresholding)

    #waits indefinitely for a key stroke
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
