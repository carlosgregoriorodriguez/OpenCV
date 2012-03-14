# USAGE:   Press 'q' to quit
#
#
#

import cv2
import numpy as np


if __name__ == "__main__":

    bw = cv2.imread("../../img/stop.jpg",0)    #read image

    bwx = np.array(bw,dtype = float)           #convert the array to floats

    bwDFT = cv2.dft(bwx)                       #APPLY DFT


    resultF = np.zeros(bwx.shape)              #Create dst pointer

    cv2.dft(bwDFT,resultF,cv2.DFT_INVERSE)     #APPLY INV DFT



    cv2.imshow("ORIGINAL",bw)
    cv2.imshow("FOURIER",bwDFT)


    cv2.imshow("FOURIER INV.",resultF)





    while True:
        
        k = cv2.waitKey(5)

        if (k == 113):    #quit on 'q'
            print "Quit"
            break
        
