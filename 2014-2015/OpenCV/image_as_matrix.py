# -*- coding: utf-8 -*-
import cv2
import algorithm
import numpy as np

__author__ = 'mimadrid'

# http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_table_of_contents_core/py_table_of_contents_core.html#py-table-of-content-core
# http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html#image-arithmetics
# http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_optimization/py_optimization.html#optimization-techniques

def mouse_callback(event,x,y,flags,param):
    if event == cv2.EVENT_MOUSEMOVE:
        print "punto1", x, y
    


if __name__ == '__main__':
        
    window_title = 'matrix'
    
    alg = algorithm.Algorithm('edi uveitis previa 11.png')
    alg.to_horizontal() 
    
    img = alg.img_horizontal
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, otsu_threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    print otsu_threshold[0,0]
    print otsu_threshold.shape    
    # si cv2.imread(..., 0) sólo escala de grises 0..255 y (332, 1031) si no, [0..255 0..255 0..255] (332, 1031, 3) 
    # y se puede dibujar con colores en la imagen 
      

    y, x = otsu_threshold.shape
    cv2.imshow('otsu', otsu_threshold)

    #Hemos comprobado que el threshold en más de una ocasión crea una línea recta horizontal en la fóvea. Para encontrar un punto céntrico, 
    #llevaremos dos puntos de coordenadas, el de más a la izquierda y el de más a la derecha,
    #para así luego poder calcular la media en el eje x
    punto1 = (0, 0)
    punto2 = (0, 0)

    #Restringimos el área para buscar en el eje de las x teniendo en cuenta que la fóvea esta siempre entre 1/3 y 2/3
    for i in xrange(x / 3, 2 * x / 3):  
         for j in xrange(y):
             
                    if otsu_threshold[j,i] == 255:
                        
                        #Actualización punto más bajo y a la derecha
                        if punto1[0] == j:
                            punto2 = (j, i)
                            
                        #Actualización de los puntos más bajos
                        if punto1[0] < j:
                            punto1 = (j, i)
                            punto2 = (j, i) 
                            
                        break    
    
    #Cálculo de la media de los valores de la x de los dos puntos
    x = (punto1[1] + punto2[1]) / 2
    y = punto1[0]
    
    cv2.circle(img, (x,y), 2, (0,0,255),3)  # draw the center of the circle
    cv2.imshow(window_title, img)    
    cv2.setMouseCallback(window_title, mouse_callback)
    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()


