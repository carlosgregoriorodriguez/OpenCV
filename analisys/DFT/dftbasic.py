# USAGE:     python dftbasic.py (img path)
#
#      Press 'q' to quit


import cv2
import cv2.cv as cv
import numpy as np
import sys

if __name__ == "__main__":

    bw = cv2.imread(sys.argv[1],0)             #read image

    bwx = np.array(bw,dtype = float)           #convert the array to floats

    bwDFT = cv2.dft(bwx)                       #APPLY DFT and DCT
    bwDCT = cv2.dct(bwx)

    auxF = cv2.dft(bwDFT,flags = cv.CV_DXT_INV_SCALE)
    auxC = cv2.dct(bwDCT,flags = cv.CV_DXT_INV_SCALE)
    #resultC = np.zeros(bwx.shape)

    resultF = np.array(auxF, dtype = "uint8")
    resultC = np.array(auxC, dtype = "uint8")
    #cv2.dct(bwDCT,resultC,cv2.DCT_INVERSE)

    cv2.imshow("ORIGINAL",bw)
    #cv2.imshow("FOURIER",bwDFT)
    #cv2.imshow("COSINE",bwDCT)

    cv2.imshow("FOURIER INV.",resultF)
    cv2.imshow("COSINE INV.",resultC)


    #cv2.imshow("SUM",bwDCT + bwDFT)

    while True:
        
        k = cv2.waitKey(5)

        if (k == 113):    #quit on 'q'
            print "Quit"
            break
        
