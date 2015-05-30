# -*- coding: utf-8 -*-

import argparse
import os
import glob
import shutil


def crear_carpeta(carpeta_procesada):
    if not os.path.exists(carpeta_procesada):
        os.mkdir(carpeta_procesada)

def procesar_archivo(img_name, carpeta_procesada, debug_mode, run_algorithm):
    crear_carpeta(carpeta_procesada)
    shutil.copy(img_name, carpeta_procesada + os.sep + img_name)
    os.chdir(carpeta_procesada)
    run_algorithm(img_name, debug_mode)
    os.remove(img_name)
    os.chdir('..')


def procesar_carpeta(carpeta_procesada, debug_mode, run_algorithm):
    img_names = []
    img_types = ('*.bmp', '*.tif', '*.png')
    crear_carpeta(carpeta_procesada)
    for img_type in img_types:
            img_names.extend(glob.glob(img_type))
            for img_name in img_names:
                procesar_archivo(img_name, carpeta_procesada, debug_mode, run_algorithm)

parser = argparse.ArgumentParser(description='Programa para la medición automática de la coroides')
parser.add_argument('-p', '--pasos', action='store_true', help='guardar todos los pasos intermedios del procesamiento')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-a', '--archivos', type=str, nargs='+', help='archivos a procesar por el programa')
group.add_argument('-c', '--carpetas', type=str, nargs='+', help='carpetas a procesar por el programa')
carpeta_procesada = 'PROCESADAS'

if __name__ == '__main__':

    args = parser.parse_args()

    if args.pasos:
        print 'opción pasos'
    if args.archivos:
        print 'opción archivos'
        for archivo in args.argumentos:
            procesar_archivo(archivo, carpeta_procesada, aplicar_algoritmo)

    if args.carpetas:
        print 'opción carpetas'
        for carpeta in args.argumentos:
            os.chdir(carpeta)
            procesar_carpeta(carpeta_procesada, aplicar_algoritmo())
            os.chdir('..')