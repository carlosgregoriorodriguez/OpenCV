# -*- coding: utf-8 -*-

# Copyright © 2015, Miguel Madrid Mencía and Daniel Arnao Rodríguez. All rights reserved.
#
# Developed by:
#
# Miguel Madrid Mencía and Daniel Arnao Rodríguez
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# “Software”), to deal with the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimers.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimers in the
# documentation and/or other materials provided with the distribution.
# Neither the names of Miguel Madrid Mencía and Daniel Arnao Rodríguez,
# nor the names of its contributors may be used to endorse or promote
# products derived from this Software without specific prior written
# permission.  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE
# SOFTWARE.

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