import cv2


def dummy(v):
   print "value "+str(v)

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    #create the window where the boxFiltered image will be shown
    cv2.namedWindow("boxFilter")

    #create a trackbar that controlls the ksize.X value
    cv2.createTrackbar("ksize.X","boxFilter",1,200,dummy)
    
    #create a trackbar that controlls the ksize.Y value
    cv2.createTrackbar("ksize.Y","boxFilter",1,200,dummy)

    #create a trackbar that controlls the ksize.Y value
    #cv2.createTrackbar("ddepth","boxFilter",2,10,dummy)

  
    while True:

        f,img = camera.read()

        #boxFilter the image with the selected parameters in the trackbars
        img2 = cv2.boxFilter(img,-1,(cv2.getTrackbarPos("ksize.X","boxFilter"),cv2.getTrackbarPos("ksize.Y","boxFilter")))

        cv2.imshow("boxFilter",img2)

        if (cv2.waitKey(5) != -1):    
            break
