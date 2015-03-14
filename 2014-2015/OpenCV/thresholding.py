import cv2
from matplotlib import pyplot as plt

__author__="mimadrid"

drawing = False
mode = True
ix, iy = -1, -1
imgName = 'poros papila'
img = cv2.imread(imgName+'.bmp', 0)
windowTitle = 'Imagen'
#windowThres = 'Thresholding'
windowThres = windowTitle

value = 127
maxValue = 255
thres = cv2.THRESH_BINARY

def fValue(x):
    global value, maxValue, thres, img
    value = x
    if (thres is None):
        filtro = img

    else:
        ret, filtro = cv2.threshold(img,value, maxValue, thres)
    cv2.imshow(windowTitle, filtro)

def fMaxValue(x):
    global maxValue, value, thres, img
    maxValue = x
    if (thres is None):
        filtro = img

    else:
        ret, filtro = cv2.threshold(img,value, maxValue, thres)
    cv2.imshow(windowTitle, filtro)

def thresholding(x):
    global thres, value, maxValue, img
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
    cv2.imshow(windowTitle, filtro)


def mouse_event(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, windowTitle
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'Left button down'
        drawing = True
        ix,iy = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        print x,y
        if drawing == True:
            if mode == True:
                cv2.line(img,(ix,iy),(x,y),(255,0,0),5)
            else:
                cv2.circle(img,(x,y),5,(0,0,255),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        print 'Left button up'
        drawing = False
        if mode == True:
            cv2.line(img,(ix,iy),(x,y),(255,0,0),5)
        else:
            cv2.circle(img,(x,y),5,(0,0,255),-1)

    elif event == cv2.EVENT_FLAG_LBUTTON:
        print "Left button"
    elif event == cv2.EVENT_LBUTTONDBLCLK:
        print "Left double button"
    elif event == cv2.EVENT_FLAG_RBUTTON:
        print "Right button"
    elif event == cv2.EVENT_RBUTTONDBLCLK:
        print "Right double button"
    cv2.imshow(windowTitle,img)


if __name__ == "__main__":
    # 0 = cv2.IMREAD_GRAYSCALE
    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(img,'Prueba',(110, 650), font, 2,(255,0,255),2, 255)
    cv2.setMouseCallback(windowTitle, mouse_event)

    cv2.namedWindow(windowThres, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Value', windowThres, value, maxValue, fValue)
    cv2.createTrackbar('MaxValue', windowThres, maxValue, maxValue, fMaxValue)

    cv2.createTrackbar('NORMAL\nTHRESH_BINARY\nTHRESH_BINARY_INV\nTHRESH_TRUNC\nTHRESH_TOZERO\nTHRESH_TOZERO_INV\n', windowThres,0, 5, thresholding)

    #plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    #plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    #plt.show()
    #waits indefinitely for a key stroke
    cv2.imshow(windowTitle, img)
    while True:

        #key = cv2.waitKey(0)
        # 64 bits
        key = cv2.waitKey(0) & 0xFF
        if key == ord('m'):
            mode = not mode
        # 27 = ESC
        if key==27:
            #cv2.destroyAllWindows()
            cv2.destroyWindow(windowTitle)
            #cv2.imwrite(imgName +'.png', img)
            break
