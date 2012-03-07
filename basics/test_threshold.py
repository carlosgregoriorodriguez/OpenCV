import cv2


def dummy(v):
   print "value "+str(v)

if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    #create the window where the thresholded image will be shown
    cv2.namedWindow("threshold")

    #create a trackbar that controlls the thresh value
    cv2.createTrackbar("thresh","threshold",0,256,dummy)
    
    #create a trackbar that controlls the maxval value
    cv2.createTrackbar("maxval","threshold",0,256,dummy)

    #create a trackbar that controlls the type of threshold that is used 
    cv2.createTrackbar("type","threshold",0,4,dummy)
    d = {0:(cv2.THRESH_BINARY,"BINARY"),
        1:(cv2.THRESH_BINARY_INV,"BINARY_INV"),
        2:(cv2.THRESH_TRUNC,"TRUNC"),
        3:(cv2.THRESH_TOZERO,"TOZERO"),
        4:(cv2.THRESH_TOZERO_INV,"TOZERO_INV")}

    while True:

        f,img = camera.read()

        #threshold the image with the selected parameters in the trackbars
        retVal,img2 = cv2.threshold(img,cv2.getTrackbarPos("thresh","threshold"),cv2.getTrackbarPos("maxval","threshold"),d[cv2.getTrackbarPos("type","threshold")][0])

        cv2.putText(img2,d[cv2.getTrackbarPos("type","threshold")][1],(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,1,1,8,False)
        cv2.imshow("threshold",img2)

        if (cv2.waitKey(5) != -1):    
            break
