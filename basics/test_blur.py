import cv2


def dummy(v):
   print "value "+str(v)

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    #create the window where the blurred image will be shown
    cv2.namedWindow("blur")

    #create a trackbar that controlls the ksize.X value
    cv2.createTrackbar("ksize.X","blur",1,200,dummy)
    
    #create a trackbar that controlls the ksize.Y value
    cv2.createTrackbar("ksize.Y","blur",1,200,dummy)

  
    while True:

        f,img = camera.read()

        #blur the image with the selected parameters in the trackbars
        img2 = cv2.blur(img,(cv2.getTrackbarPos("ksize.X","blur"),cv2.getTrackbarPos("ksize.Y","blur")))

        cv2.imshow("blur",img2)

        if (cv2.waitKey(5) != -1):    
            break
