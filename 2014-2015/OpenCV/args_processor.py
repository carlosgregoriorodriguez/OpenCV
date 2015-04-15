# -*- coding: utf-8 -*-

import argparse
import os
import glob
import cv2
import shutil
# shutil.rmtree(carpeta_procesada)


def crear_carpeta(carpeta_procesada):
    if not os.path.exists(carpeta_procesada):
        os.mkdir(carpeta_procesada)

def aplicar_algoritmo(img_name, carpeta_procesada):
    image = cv2.imread(img_name)
    cv2.imshow(img_name, image)
    # cv2.imwrite(os.path.splitext(img_name)[0] + '_PROCESADA' + os.path.splitext(img_name)[1], image)
    os.chdir(carpeta_procesada)
    cv2.imwrite(img_name, image)
    os.chdir('..')


def procesar_archivo(img_name, carpeta_procesada):
    crear_carpeta(carpeta_procesada)
    aplicar_algoritmo(img_name, carpeta_procesada)


def procesar_carpeta(carpeta_procesada):
    img_names = []
    img_types = ('*.bmp', '*.tif', '*.png')
    crear_carpeta(carpeta_procesada)
    for img_type in img_types:
            img_names.extend(glob.glob(img_type))
            for img_name in img_names:
                aplicar_algoritmo(img_name, carpeta_procesada)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Programa para la medición automática de la coroides')
    parser.add_argument('argumentos', type=str, nargs='+', help='argumentos a procesar por el programa')
    parser.add_argument('-p', '--pasos', action='store_true', help='guardar todos los pasos intermedios del procesamiento')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--archivos', action='store_true', help='archivos a procesar por el programa')
    group.add_argument('-c', '--carpetas', action='store_true', help='carpetas a procesar por el programa')

    args = parser.parse_args()

    carpeta_procesada = 'PROCESADAS'

    if args.pasos:
        print 'opción pasos'
    if args.archivos:
        print 'opción archivos'
        for archivo in args.argumentos:
            procesar_archivo(archivo, carpeta_procesada)

    if args.carpetas:
        print 'opción carpetas'
        for carpeta in args.argumentos:
            os.chdir(carpeta)
            procesar_carpeta(carpeta_procesada)
            os.chdir('..')