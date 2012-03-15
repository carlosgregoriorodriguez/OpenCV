# Program that combines pyrDown and the DFT calculating the fps to observe
#        the cost of the operations done.
#
# USAGE:   python DFTpyr.py N            - for webcam
#          python DFTpyr.py (image path) - for image
#
#  Shows the original, dft + dft_inv , dft + dft_inv reduced by pyrDown 
#              and dft + dft_inv reduced twice by pyrDown
#
#   Press 'q' to quit

import cv2
import cv2.cv as cv
import numpy as np
import sys , time

if __name__ == "__main__":

    video = False if sys.argv[1] != 'N' else True

    if video:
        camera = cv2.VideoCapture(0)

    else:
        img = cv2.imread(sys.argv[1],0)

    while True:

        if video:
            f,img = camera.read()
            img = cv2.cvtColor(img, 7)
            
    
        imgx = np.array(img,dtype = float)
        imgDFT = cv2.dft(imgx)
        imgDFTpyr = cv2.dft(cv2.pyrDown(imgx))       #APPLY DFT on pyrDown
        imgDFTpyr2 = cv2.dft(cv2.pyrDown(cv2.pyrDown(imgx))) #on double pyrDown

        aux = cv2.dft(imgDFT, flags = cv.CV_DXT_INV_SCALE)
        auxpyr = cv2.dft(imgDFTpyr, flags = cv.CV_DXT_INV_SCALE)
        auxpyr2 = cv2.dft(imgDFTpyr2, flags = cv.CV_DXT_INV_SCALE)

        result = np.array(aux, dtype ="uint8")
        resultpyr = np.array(auxpyr, dtype ="uint8")
        resultpyr2 = np.array(auxpyr2, dtype ="uint8")

        if video:
            fps = 999.9
            cv2.putText(img=img, text="%d fps"%fps, org=(20, 20), 
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0,
                        color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)
            cv2.putText(img=img, text="%d fps"%fps, org=(20, 20), 
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                        color=(255,255,255), thickness = 1, linetype=cv2.CV_AA) 
            
            cv2.putText(img=result, text="%d fps"%fps, org=(20, 20), 
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                        color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)
            cv2.putText(img=result, text="%d fps"%fps, org=(20, 20), 
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                        color=(255,255,255), thickness = 1, linetype=cv2.CV_AA) 
            
            cv2.putText(img=resultpyr, text="%d fps"%fps, org=(20, 20), 
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                        color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)
            cv2.putText(img=resultpyr, text="%d fps"%fps, org=(20, 20), 
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                        color=(255,255,255), thickness = 1, linetype=cv2.CV_AA) 
            
            cv2.putText(img=resultpyr2, text="%d fps"%fps, org=(20, 20), 
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                        color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)
            cv2.putText(img=resultpyr2, text="%d fps"%fps, org=(20, 20), 
                        fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                        color=(255,255,255), thickness = 1, linetype=cv2.CV_AA) 

        #print type(img)
        cv2.imshow("ORIGINAL",img)
        cv2.imshow("DFT -> DFT_INV",result)
        cv2.imshow("DFT -> DFT_INV (on PyrDown)",resultpyr)
        cv2.imshow("DFT -> DFT_INV (on double PyrDown)",resultpyr2)

        k = cv2.waitKey(5)

        if (k == 113):    #quit on 'q'
            print "Quit"
            break        

