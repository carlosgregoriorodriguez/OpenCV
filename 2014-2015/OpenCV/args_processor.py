# -*- coding: utf-8 -*-

import argparse
import os
import glob
import cv2
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Programa para la medición automática de la coroides')
    parser.add_argument('argumentos', type=str, nargs='+', help='argumentos a procesar por el programa')
    parser.add_argument('-p', '--pasos', action='store_true', help='guardar todos los pasos intermedios del procesamiento')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--archivos', action='store_true', help='archivos a procesar por el programa')
    group.add_argument('-c', '--carpetas', action='store_true', help='carpetas a procesar por el programa')

    args = parser.parse_args()

    img_types = ('*.bmp', '*.tif', '*.png')
    img_names = []

    carpeta_procesadas = 'PROCESADAS'

    if args.pasos:
        print 'opción pasos'
    if args.archivos:
        print 'opción archivos'
    if args.carpetas:
        print 'opción carpetas'
        for x in args.argumentos:
            os.chdir(x)
            if os.path.exists(carpeta_procesadas):
                shutil.rmtree(carpeta_procesadas)
            os.mkdir(carpeta_procesadas)
            for img_type in img_types:
                img_names.extend(glob.glob(img_type))
                for img_name in img_names:
                    image = cv2.imread(img_name)
                    cv2.imshow(img_name, image)
                    # cv2.imwrite(os.path.splitext(img_name)[0] + '_PROCESADA' + os.path.splitext(img_name)[1], image)
                    os.chdir(carpeta_procesadas)
                    cv2.imwrite(img_name, image)
                    os.chdir('..')