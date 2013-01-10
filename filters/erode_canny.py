import cv2
import numpy as np
import sys

def dummy(value):
   print value

def help():
   print ">"*40
   print "Usage:"
   print "continue to work ............"
   print "target: to isolate the butterflies from the background"
   print "<"*40

if __name__ == "__main__":
    help()
    video = False;
    filename = '../img/stop.jpg';
    cam = False;
    img = None;
    if (len(sys.argv)>1):
        try:
            x = int(sys.argv[1])
            cam = cv2.VideoCapture(int(sys.argv[1]));
            cam.set(3, 640);
            cam.set(4, 480);
            video = True;
        except ValueError:
            filename = sys.argv[1];

    cv2.namedWindow('config', cv2.cv.CV_WINDOW_NORMAL); 
    cv2.createTrackbar("erode iter", "config", 3,7, dummy)
    cv2.createTrackbar("canny tresh1", 'config',250,600, dummy);
    cv2.createTrackbar("canny tresh2", 'config',30,600, dummy);   
    while True:		
        if (video):
            f,img = cam.read();
        else:
            img = cv2.imread(filename);

            
        img_erode = cv2.erode(img,kernel=None,iterations=cv2.getTrackbarPos("erode iter","config"))    
        
        imgbn = cv2.cvtColor(img_erode,cv2.cv.CV_BGR2GRAY) 

        print "BN"
        print imgbn
        print imgbn.shape, imgbn.dtype
        
        canny = cv2.Canny(imgbn,cv2.getTrackbarPos("canny tresh1","config"), cv2.getTrackbarPos("canny tresh2","config"))
        
        print "Canny"
        print canny
        print canny.shape, canny.dtype
        
        rawcontours,hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

        cv2.drawContours(img, rawcontours, -1, (255,0,0), 1, cv2.CV_AA);

        cv2.imshow('erode',img_erode)
        cv2.imshow('img', img)
        key = cv2.waitKey(5);
        if (key != -1):
            if key == 112 : #tecla p 
                outimg = "output_"+str(int(time.time()))+".jpeg"
                print "output image:", outimg
                cv2.imwrite(outimg, img)
            if key & 255 == 113 : #tecla q
                break
