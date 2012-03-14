#USAGE:     python dftbasic.py (img path)
#
#      Press 'q' to quit


import cv2
import cv2.cv as cv
import numpy as np
import sys

if __name__ == "__main__":

    img = cv2.imread(sys.argv[1],0)             #read image
    cv2.imshow("ORIGINAL",img)

    imgx = np.array(img,dtype = float)           #convert the array to floats

    #APPLY DFT and DCT
    imgDFT = cv2.dft(imgx)
    imgDCT = cv2.dct(imgx)
    imgDFTINV = cv2.dft(imgx, flags = cv2.DFT_INVERSE)

    auxFC = cv2.dct(imgDFT,flags = cv.CV_DXT_INV_SCALE)
    resultFC = np.array(auxFC, dtype = "uint8")
    cv2.imshow("DFT -> DCT_INV",resultFC)

    auxCF = cv2.dct(imgDCT,flags = cv.CV_DXT_INV_SCALE)
    resultCF = np.array(auxCF, dtype = "uint8")
    cv2.imshow("DCT -> DFT_INV",resultCF)

    auxF2F = cv2.dft(imgDFT*2,flags = cv.CV_DXT_INV_SCALE)
    resultF2F = np.array(auxF2F, dtype = "uint8")
    cv2.imshow("DFT*2 -> DFT_INV/2",resultF2F/2)

    auxC2C = cv2.dct(imgDCT*2,flags = cv.CV_DXT_INV_SCALE)
    resultC2C = np.array(auxC2C, dtype = "uint8")
    cv2.imshow("DCT*2 -> DCT_INV",resultC2C)

    auxFINV = cv2.dft(imgDFTINV, flags = cv2.DFT_SCALE)
    resultFINV = np.array(auxFC, dtype = "uint8")
    cv2.imshow("DFT_INV -> DFT",resultFINV)



    while True:
        
        k = cv2.waitKey(5)

        if (k == 113):    #quit on 'q'
            print "Quit"
            break
        
