# USAGE:   Press 'q' to quit
#
#
#

import cv2
import numpy as np


if __name__ == "__main__":

    ori = cv2.imread("../../img/stop.jpg",0)    #read image

    bw = cv2.pyrDown(-ori)

    bwx = np.array(bw,dtype = float)           #convert the array to floats
    bwx2 = np.array(ori,dtype = float)          #convert the array to floats

    bwDFT = cv2.dft(bwx)                       #APPLY DFT
    bwDFT2 = cv2.dft(bwx2)                       #APPLY DFT


    resultF = np.zeros(bwx.shape)
    resultF2 = np.zeros(bwx2.shape)

    cv2.dft(bwDFT,resultF,cv2.DFT_INVERSE)
    cv2.dft(bwDFT2,resultF2,cv2.DFT_INVERSE)



    cv2.imshow("ORIGINAL",bw)
    cv2.imshow("FOURIER",bwDFT)
    cv2.imshow("FOURIER2",bwDFT2)


    cv2.imshow("FOURIER INV.",-resultF)
    cv2.imshow("FOURIER  INV.",resultF2)





    while True:
        
        k = cv2.waitKey(5)

        if (k == 113):    #quit on 'q'
            print "Quit"
            break
        
