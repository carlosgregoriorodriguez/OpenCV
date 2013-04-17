import cv2
import numpy as np
import sys

def dummy(pos):
    pos
 
if __name__ == "__main__":
    
    img = cv2.imread(sys.argv[1])
    cv2.imshow('image',img)
    
    cv2.namedWindow('config', cv2.cv.CV_WINDOW_NORMAL);

    cv2.createTrackbar('canny tresh1', 'config',482,600,dummy)
    cv2.createTrackbar('canny tresh2', 'config', 0,600, dummy)
    cv2.createTrackbar('draw on original','config',1,1,dummy)
    cv2.createTrackbar('show one contour','config',1,1,dummy) 
   

    i = 0 
    print 'l'+str(i)
    if(cv2.getTrackbarPos("draw on original","config") == 1):
        imgToShow = img.copy();
    else:
        imgToShow = np.zeros(img.shape);

    while True:
        img2 = img.copy()
        imgcanny = cv2.Canny(cv2.cvtColor(img2,cv2.cv.CV_RGB2GRAY), cv2.getTrackbarPos("canny tresh1","config"), cv2.getTrackbarPos("canny tresh2","config"))
        contours, hierarchy = cv2.findContours(imgcanny.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cv2.approxPolyDP(contour, 1, True) for contour in contours];
        if (cv2.getTrackbarPos('show one contour', 'config') == 1):
            if(cv2.getTrackbarPos("draw on original","config") == 1):
                imgToShow = img.copy();
            else:
                imgToShow = np.zeros(img.shape);

        cv2.drawContours(imgToShow,contours, max(0,i), (0,0,255),1, cv2.CV_AA)
        cv2.imshow('contour',imgToShow)
 
        k = cv2.waitKey(5)
        #if press p shown other contour
        if (k == 112):
            i = i+1
            if(len(contours)>i):
                print 'l'+str(i)
            else:
                i = 0
                print 'l'+str(i)
            
        # if press a shown the area of the contour
        elif (k == 97):
            area = cv2.contourArea(contours[i])
            print '     area: '+str(area)

        # if press z shown the perimeter of the contour
        # EL PERIMETRO LO CALCULA MAL

       # elif (k == 122):
        #    perimeter = cv2.arcLength(contours[i], False)
         #   print '     perimeter: '+str(perimeter)
        if (k == 27):
            break
