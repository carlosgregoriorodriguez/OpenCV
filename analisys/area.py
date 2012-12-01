import cv2
import numpy as np
import sys

def dummy(pos):
    pos
 
def onMouse (event, x, y, flags, param):
    global point
    if flags & cv2.EVENT_FLAG_LBUTTON:
        print (x,y)
        point = x,y
        update()

def update(dummy=None):
    global img2, imgToShow
    mask[:] = 0 
    img2 = img.copy()
    if cv2.getTrackbarPos('black or white','config') == 0:
        color = (0,0,0)
    else: color = (255,255,255)

    cv2.floodFill(img2, mask, point, color, (cv2.getTrackbarPos("low","config"), )*3, (cv2.getTrackbarPos("hi","config"), )*3,cv2.FLOODFILL_FIXED_RANGE)        
    cv2.circle(img2, point, 3, color, -1)
    imgToShow = img2.copy()
    cv2.imshow("image",img2)


if __name__ == "__main__":
    
    img = cv2.imread(sys.argv[1])
    cv2.imshow('image',img)
    img2 = img.copy()

    h = img.shape[0]
    w = img.shape[1]
    mask = np.zeros((h+2,w+2), np.uint8)
    point = None


    cv2.namedWindow('config', cv2.cv.CV_WINDOW_NORMAL);

    cv2.createTrackbar('canny tresh1', 'config',482,600,dummy)
    cv2.createTrackbar('canny tresh2', 'config', 0,600, dummy)
   # cv2.createTrackbar('level','config', 1,10, dummy)
    cv2.createTrackbar('draw on original','config',1,1,dummy)
    cv2.createTrackbar('show one contour','config',1,1,dummy) 
    cv2.createTrackbar('low', 'config', 20, 255, update)
    cv2.createTrackbar('hi', 'config', 20, 255, update) 
    cv2.createTrackbar('black or white','config', 1, 1, update)

    cv2.setMouseCallback("image",onMouse)


    i = 0 
    print 'l'+str(i)
    if(cv2.getTrackbarPos("draw on original","config") == 1):
        imgToShow = img2.copy();
    else:
        imgToShow = np.zeros(img.shape);

    while True:
        img3 = img2.copy()
        imgcanny = cv2.Canny(cv2.cvtColor(img3,cv2.cv.CV_RGB2GRAY), cv2.getTrackbarPos("canny tresh1","config"), cv2.getTrackbarPos("canny tresh2","config"))
        contours, hierarchy = cv2.findContours(imgcanny.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cv2.approxPolyDP(contour, 1, True) for contour in contours];
        if (cv2.getTrackbarPos('show one contour', 'config') == 1):
            if(cv2.getTrackbarPos("draw on original","config") == 1):
                imgToShow = img2.copy();
            else:
                imgToShow = np.zeros(img.shape);

        cv2.drawContours(imgToShow,contours, max(0,i), (0,0,255),1, cv2.CV_AA)
        cv2.imshow('contour',imgToShow)
 
        k = cv2.waitKey(5)
        #if press p shown other contour
        if (k == 112):
            if(len(contours)>i):
                print 'l'+str(i)
                i = i +1
                cv2.drawContours(imgToShow,contours[i], -1, (0,0,255),2, cv2.CV_AA)
                cv2.imshow('contour',imgToShow)
            else: i = -1
        # if press a shown the area of the contour i
        elif (k == 97):
            area,p = cv2.contourArea(contours[i])
            print '     area: '+str(area)+" "+str(p)


        # if press z shown the perimeter of the contour i
        # EL PERIMETRO LO CALCULA MAL!!!
       # elif (k == 122):
        #    perimeter = cv2.arcLength(contours[i], False)
         #   print '     perimeter: '+str(perimeter)
        if (k == 27):
            break

    
