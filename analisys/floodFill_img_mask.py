import numpy as np
import cv2
import sys

help_message = '''USAGE: floodfill.py [<image>]

Click on the image to set seed point

Keys:
  f     - toggle floating range
  c     - toggle 4/8 connectivity
  ESC   - exit
'''

if __name__ == '__main__':
    print help_message
    
    
    img = cv2.imread(sys.argv[1])
    h, w = img.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    seed_pt = None
    fixed_range = True
    connectivity = 4

    def update(dummy=None):
        if seed_pt is None:
            cv2.imshow('floodfill', img)
            return
        flooded = img.copy()
        
        lo = cv2.getTrackbarPos('lo', 'floodfill')
        hi = cv2.getTrackbarPos('hi', 'floodfill')
        flags = connectivity
        if fixed_range:
            flags |= cv2.FLOODFILL_FIXED_RANGE

        imgbn = cv2.cvtColor(img,cv2.cv.CV_BGR2GRAY) 
        canny = cv2.Canny(imgbn,cv2.getTrackbarPos("canny tresh1","floodfill"), cv2.getTrackbarPos("canny tresh2","floodfill"))
        cv2.imshow("canny",canny)
        mask[1:h+1,1:w+1] = canny 
        cv2.floodFill(flooded, mask, seed_pt, (255, 255, 255), (lo,)*3, (hi,)*3, flags)
        cv2.circle(flooded, seed_pt, 5, (0, 0, 255), -1)
        cv2.imshow('floodfill', flooded)

    def onmouse(event, x, y, flags, param):
        global seed_pt
        if flags & cv2.EVENT_FLAG_LBUTTON:
            seed_pt = x, y
            update()

    update()
    cv2.setMouseCallback('floodfill', onmouse)
    cv2.createTrackbar('lo', 'floodfill', 20, 255, update)
    cv2.createTrackbar('hi', 'floodfill', 20, 255, update) 
    cv2.createTrackbar("canny tresh1", 'floodfill', 250, 600, update);
    cv2.createTrackbar("canny tresh2", 'floodfill', 30, 600, update);

    while True:        
        ch = cv2.waitKey(5)
        if ch == 27:
            break
        if ch == ord('f'):
            fixed_range = not fixed_range
            print 'using %s range' % ('floating', 'fixed')[fixed_range]
        if ch == ord('c'):
            connectivity = 12-connectivity
            print 'connectivity =', connectivity            
        img = cv2.imread(sys.argv[1])
        img = cv2.medianBlur(img,3)
        update()
