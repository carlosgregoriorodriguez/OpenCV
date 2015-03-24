# -*- coding: utf-8 -*-
import cv2

__author__ = 'mimadrid'

# http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_table_of_contents_core/py_table_of_contents_core.html#py-table-of-content-core
# http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
# http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_image_arithmetics/py_image_arithmetics.html#image-arithmetics
# http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_optimization/py_optimization.html#optimization-techniques


if __name__ == '__main__':
        
    window_title = 'matrix'
    img = cv2.imread('edi uveitis previa 11.png', 0)
    
    print img[0,0]
    print img.shape    
    # si cv2.imread(..., 0) sólo escala de grises 0..255 y (332, 1031) si no, [0..255 0..255 0..255] (332, 1031, 3) 
    # y se puede dibujar con colores en la imagen 
    cv2.circle(img,(200,200),5,(0,255,0),1)  # draw the outer circle
    cv2.circle(img,(200,200),1,(0,0,255),1)  # draw the center of the circle
    cv2.imshow(window_title, img)
    cv2.waitKey(0) & 0xFF
    cv2.destroyAllWindows()


