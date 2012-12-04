import cv2
import sys
import numpy as np

if __name__ == '__main__':
    
    if (len(sys.argv)==2):
        name_images = [sys.argv[1]]
    else:
        name_images = ['BMC-1903_D.jpg', 'BMC-1923_D.jpg', 'BMC-1943_D.jpg', 'BMC-1956_D.jpg', 'BMC-1966_D.jpg', 'BMC-1905_D.jpg', 'BMC-1925_D.jpg', 'BMC-1944_D.jpg', 'BMC-1957_D.jpg', 'BMC-1968_D.jpg', 'BMC-1926_D.jpg', 'BMC-1946_D.jpg', 'BMC-1958_D.jpg', 'BMC-1969_D.jpg', 'BMC-1907_D.jpg', 'BMC-1933_D.jpg', 'BMC-1948_D.jpg',  'BMC-1959_D.jpg', 'BMC-1970_D.jpg', 'BMC-1913_D.jpg', 'BMC-1951_D.jpg', 'BMC-1960_D.jpg', 'BMC-1971_D.jpg', 'BMC-1916_D.jpg', 'BMC-1936_D.jpg', 'BMC-1953_D.jpg', 'BMC-1963_D.jpg', 'BMC-1972_D.jpg', 'BMC-1918_D.jpg', 'BMC-1954_D.jpg', 'BMC-1964_D.jpg', 'BMC-1919_D.jpg', 'BMC-1942_D.jpg', 'BMC-1955_D.jpg', 'BMC-1965_D.jpg']
    
    images = []
    for img in name_images:
        if (len(name_images)!=1):
            name = 'butterflies/'+str(img)
        else:
            name = sys.argv[1]
        images = images + [cv2.imread(name)]

    for img in images:

        template = cv2.imread('qp2.jpg')
        imgfound = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
        minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(imgfound)
        cv2.rectangle(img,(minLoc[0]-40,minLoc[1]-40),(minLoc[0]+template.shape[1]+40,minLoc[1]+template.shape[0]+40),(0,255,0))
        cv2.imshow('img',img)
       # cv2.imshow('template',imgfound)

        imgt = np.zeros(img.shape,np.uint8)+255
        imgt[minLoc[1]-40:minLoc[1]+template.shape[0]+40,minLoc[0]-40:minLoc[0]+template.shape[1]+40] = img[minLoc[1]-40:minLoc[1]+template.shape[0]+40,minLoc[0]-40:minLoc[0]+template.shape[1]+40]
        #cv2.imshow('imgt',imgt)
        #imgthres = cv2.adaptiveThreshold(cv2.cvtColor(imgt,cv2.cv.CV_RGB2GRAY),255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,599,60)
        v, imgthres = cv2.threshold(imgt,86,256,cv2.THRESH_BINARY_INV)
        #cv2.imshow('imgthres',imgthres)
        imgcanny = imgthres.copy()
        imgcanny = cv2.Canny(cv2.cvtColor(imgcanny,cv2.cv.CV_RGB2GRAY), 147,600)
        #cv2.imshow('canny',imgcanny)

        contours, hierarchy = cv2.findContours(imgcanny.copy(),cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cv2.approxPolyDP(contour, 1, True) for contour in contours];

        final_rect = [0,0,0,0]
        rectangles = []
        for contour in contours:
            minrect = cv2.boundingRect(contour)
            area = minrect[2]*minrect[3]
            if area < 100800-100 and minrect[2]>minrect[3]*2 and area>10000 and minrect[2]/minrect[3]>2 and minrect[2]/minrect[3]< 4 :
                rectangles = rectangles + [minrect]
                final_rect = minrect
        if (len(rectangles)>1):
            dist = 5
            for i in range(len(rectangles)):
                if (dist > abs(rectangles[i][2]/rectangles[i][3]-3.5)):
                    dist = abs(rectangles[i][2]/rectangles[i][3]-3.5)
                    final_rect = rectangles[i]
                
        cv2.rectangle(img,(final_rect[0],final_rect[1]),(final_rect[2]+final_rect[0],final_rect[3]+final_rect[1]),(0,0,255))
        cv2.imshow('img',img)
    
        k = cv2.waitKey(0)
           # if (k == 122):
                #cv2.imwrite('foto.jpg',imgt)
