#! /usr/bin/python
# -*- coding: utf-8 -*-
# opencv 2.3.1

import cv2
import sys
          
if __name__ == "__main__":

    

    
    #trying imread with different parameters
    #Python: cv2.imread(filename[, flags]) → retval
    #for flags>0 there are surprises, see later
    imgInGrey = cv2.imread(sys.argv[1],0)

    imgInColor = cv2.imread(sys.argv[1],1)

    imgAsIs = cv2.imread(sys.argv[1],-1)
    
    imgAsIs2 = cv2.imread(sys.argv[1],-2)

    #since API this should be in color... but surprise!!
    imgOther =cv2.imread(sys.argv[1],10)

    #assumption for flags>0, flags=odd => color, flags=even => bw
    imgOther2 = cv2.imread(sys.argv[1],9)

    #see the differences
    cv2.imshow("img in grey",imgInGrey)
    cv2.imshow("img in color",imgInColor)
    cv2.imshow("img as is",imgAsIs)
    cv2.imshow("img as is 2",imgAsIs2)
    cv2.imshow("img other",imgOther)
    cv2.imshow("img other 2",imgOther2)

    #all the same type
    print type(imgInGrey)
    print type(imgInColor)
    print type(imgAsIs)
    print type(imgOther)






    #some blurring
    #Python: cv2.blur(src, ksize[, dst[, anchor[, borderType]]]) → dst¶
    #what is anchor?
    #dst ignored

    #trying different ksizes
    imgBlurredBW0 = cv2.blur(imgInGrey,(5,5))
    cv2.imshow("imgBlurredBW0",imgBlurredBW0);

    #imgBlurredBW1 = cv2.blur(imgInGrey,(5,5),DEFAULT)
    #imgBlurredBW1 = cv2.blur(imgInGrey,(5,5),BORDER_DEFAULT)
    #cv2.imshow("imgBlurredBW1",imgBlurredBW1);

    imgBlurredBW2 = cv2.blur(imgInGrey,(10,10))
    cv2.imshow("imgBlurredBW2",imgBlurredBW2);

    imgBlurredBW3 = cv2.blur(imgInGrey,(100,100))
    cv2.imshow("imgBlurredBW3",imgBlurredBW3);

    #trying different borderTypes "BORDER_XXX". No idea where to find the values
    #imgBlurredBW4 = cv2.blur(imgInGrey,(10,10),BORDER_TRANSPARENT)
    #cv2.imshow("imgBlurredBW4",imgBlurredBW4);

    #imgBlurredBW5 = cv2.blur(imgInGrey,(10,10),BORDER_ISOLATED)
    #cv2.imshow("imgBlurredBW5",imgBlurredBW5);

    #imgBlurredBW6 = cv2.blur(imgInGrey,(10,10),BORDER_CONSTANT)
    #cv2.imshow("imgBlurredBW6",imgBlurredBW6);

    #imgBlurredBW7 = cv2.blur(imgInGrey,(10,10),BORDER_WRAP)
    #cv2.imshow("imgBlurredBW7",imgBlurredBW7);

    #imgBlurredBW8 = cv2.blur(imgInGrey,(10,10),BORDER_REFLECT_101)
    #cv2.imshow("imgBlurredBW8",imgBlurredBW8);


    #trying boxFilter
    #Python: cv2.boxFilter(src, ddepth, ksize[, dst[, anchor[, normalize[, borderType]]]]) → dst
    imgBoxF = cv2.boxFilter(imgInColor,3,(3,3))
    cv2.imshow("imgBoxF",imgBoxF)

    imgBoxF2 = cv2.boxFilter(imgInColor,2,(1,1))
    cv2.imshow("imgBoxF2",imgBoxF2)

    #API says:
    #"The call blur(src, dst, ksize, anchor, borderType) is equivalent to
    #boxFilter(src, dst, src.type(), anchor, true, borderType)."
    #I don't get what it does, it blurs too much...







    #trying copyMakeBorder
    #Python: cv2.copyMakeBorder(src, top, bottom, left, right, borderType[, dst[, value]]) → dst¶

    #border0 negro
    imgBorder0 = cv2.copyMakeBorder(imgInColor, 50, 50, 50, 50, 0)
    cv2.imshow("imgBorder0",imgBorder0)

    #border1 todo el corte es igual
    imgBorder1 = cv2.copyMakeBorder(imgInColor, 50, 50, 50, 50, 1)
    cv2.imshow("imgBorder1",imgBorder1)

    #border2 espejo
    imgBorder2 = cv2.copyMakeBorder(imgInColor, 50, 50, 50, 50, 2)
    cv2.imshow("imgBorder2",imgBorder2)

    #border3 jajajajaja
    imgBorder3 = cv2.copyMakeBorder(imgInColor, 50, 50, 50, 50, 3)
    cv2.imshow("imgBorder3",imgBorder3)

    #border4 igual que 2?
    imgBorder4 = cv2.copyMakeBorder(imgInColor, 50, 50, 50, 50, 4)
    cv2.imshow("imgBorder4",imgBorder4)

    #border5 ya no existe
    #imgBorder5 = cv2.copyMakeBorder(imgInColor, 50, 50, 50, 50, 5)
    #cv2.imshow("imgBorder5",imgBorder5)

    #border-1 tampoco existe
    #imgBorderM1 = cv2.copyMakeBorder(imgInColor, 50, 50, 50, 50, -1)
    #cv2.imshow("imgBorderM1",imgBorderM1)







    
    #saving an image
    #Python: cv2.imwrite(filename, image[, params]) → retval
    cv2.imwrite("imgBlurredBW.jpg",imgBlurredBW0)
    #fail
    #cv2.imwrite("imgBadQuality.jpeg",imgInColor,("CV_IMWRITE_JPEG_QUALITY",20))
    
    cv2.imwrite("imgOtherFormat.png",imgBlurredBW0)

    cv2.waitKey (0)






    #open questions:
    #-imencode and imdecode, what are they.
    #-how to access to properties of an image as a matrix (number of rows, cols)
    #-how to use params in imwrite!!
    #-where are the given border??
