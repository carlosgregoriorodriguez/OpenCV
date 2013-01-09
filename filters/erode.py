import cv2
import numpy as np
import sys

def help():
   print ">"*40
   print "Usage:"
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
    while True:		
        if (video):
            f,img = cam.read();
        else:
            img = cv2.imread(filename);

        img = cv2.erode(img,kernel=None,iterations=5)    
        cv2.imshow('img', img)
        key = cv2.waitKey(5);
        if (key != -1):
            if key == 112 : #tecla p 
                outimg = "output_"+str(int(time.time()))+".jpeg"
                print "output image:", outimg
                cv2.imwrite(outimg, img)
            if key & 255 == 113 : #tecla q
                break
