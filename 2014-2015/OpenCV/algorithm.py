# -*- coding: utf-8 -*-
import cv2
import numpy as np

__author__ = 'mimadrid'

'''
Algoritmo de visión computerizada para la medición del espesor de la coroides 
mediante la distancia fovea en tomografías de coherencia optica de la lámina cribosa
para la automatización del seguimiento de la uveitis.
Paso 1: Corrección de la inclinación de la imagen
Paso 2: Obtención de la fovea (mínimo de la curva)
Paso 3: Trazar la vertical que pase por dicho punto 
        y marcar la intersección con el resto de membranas
Paso 4: Hallar la distancia buscada
'''
class Algorithm:
    def __init__(self, name_img):
        self.img_original = cv2.imread(name_img)
        self.img_gray_original = cv2.cvtColor(self.img_original, cv2.COLOR_BGR2GRAY)
        self.img_horizontal = self.img_original
        self.step_one = False
    
    def to_horizontal(self):
        self.step_one = True
        # img_hough = im.copy()
        edges_canny = cv2.Canny(self.img_gray_original, 150, 200, apertureSize=3)
        lines = cv2.HoughLines(edges_canny, 1, np.pi / 180, 275)
        # http://homepages.inf.ed.ac.uk/rbf/HIPR2/hough.htm
        # http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
        # https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/houghlines.py
        for rho, theta in lines[0]:
            # a = np.cos(theta)
            # b = np.sin(theta)
            # x0 = a * rho
            # y0 = b * rho
            # x1 = int(x0 + 1000 * (-b))   # Here i have used int() instead of rounding the decimal value, so 3.8 --> 3
            # y1 = int(y0 + 1000 * (a))    # But if you want to round the number, then use np.around() function, then 3.8 --> 4.0
            # x2 = int(x0 - 1000 * (-b))   # But we need integers, so use int() function after that, ie int(np.around(x))
            # y2 = int(y0 - 1000 * (a))
            # cv2.line(img_hough, (x1, y1), (x2, y2), (0, 255, 0), 5)
 
            # Use the first not horizontal line as reference and rotate with that theta
    
            # radians to degrees (precision floar error allowed < 1)
            if abs((theta * 180 / np.pi) - 90) > 1: # 90 degrees line is horizontal, not use as reference
                # print "theta = %s\n" % (theta * 180 / np.pi)
                # http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
                rows, cols = self.img_gray_original.shape
                # rotate image to the horizontal (line of reference degrees minus 90 degrees)
                M = cv2.getRotationMatrix2D((cols / 2, rows / 2), (theta * 180 / np.pi) - 90, 1)
                self.img_horizontal = cv2.warpAffine(self.img_original, M, (cols, rows))
                if self.img_horizontal is None:
                    self.img_horizontal = self.img_original
                break
    
    def show_step (self, number):
        img = self.img_original
        title = 'Original'
        if number == 1 and self.step_one:
            img = self.img_horizontal
            title = 'Horizontal'
        cv2.imshow(title, img)
            
                
if __name__ == "__main__":
    
    algorithm = Algorithm('edi uveitis previa 11.png')
    algorithm.show_step(0)
    algorithm.to_horizontal()
    algorithm.show_step(1)
    cv2.waitKey(0) & 0xFF #  64 bits

    cv2.destroyAllWindows()
