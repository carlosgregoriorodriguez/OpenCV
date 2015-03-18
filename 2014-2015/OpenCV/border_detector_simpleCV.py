from SimpleCV import Image
import cv2

__author = "mimadrid"

#img = Image('edi uveitis previa 11.png')
windowTitle = "canny detector"
cv2_img = cv2.imread('edi uveitis final6.png')
scv_img = Image(cv2_img, cv2image=True)
scv_img = scv_img.rotate90()

def threshold(value):
    global scv_img
    # The t1 parameter is roughly the "strength" of the edge required, and the
    # value between t1 and t2 is used for edge linking.  
    output = scv_img.edges(t1=value)
    #output.show()
    cv2.imshow(windowTitle, output.getNumpyCv2())


if __name__ == "__main__":
    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Threshold', windowTitle, 0, 1000, threshold)
    #output.show()
    #imgs.addDrawingLayer(output.dl())    
    #cv2_image = scv_img.getNumpyCv2()
    #ocv_gray = cv2.cvtColor(ocv_image, cv2.cv.CV_BGR2GRAY)
    cv2.imshow(windowTitle, scv_img.getNumpyCv2())
    while True:

        # key = cv2.waitKey(0)
        # 0xFF para 64 bits
        key = cv2.waitKey(0) & 0xFF
        # 27 = ESC 113 = q
        if key == 27 or key == 113:
            cv2.destroyWindow(windowTitle)
            break
    