# -*- coding: utf-8 -*-

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Programa para la medición automática de la coroides')
    parser.add_argument('argumentos', type=str, nargs='+', help='argumentos a procesar por el programa')
    parser.add_argument('-p', '--pasos', action='store_true', help='guardar todos los pasos intermedios del procesamiento')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--archivos', action='store_true', help='archivos a procesar por el programa')
    group.add_argument('-c', '--carpetas', action='store_true', help='carpetas a procesar por el programa')

    args = parser.parse_args()

    if args.pasos:
        print 'pasos'
    if args.archivos:
        print 'archivos'
    if args.carpetas:
        print 'carpetas'
    for x in args.argumentos:
        print x
