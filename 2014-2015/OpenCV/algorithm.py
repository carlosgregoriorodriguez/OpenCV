# -*- coding: utf-8 -*-
import cv2
import numpy
import roi_utils
import os
import args_processor

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
    def __init__(self, image_name):

        img_file = cv2.imread(image_name)
        roi = roi_utils.to_roi(img_file)
        self.image_name = image_name
        self.img_original = roi.copy()
        self.img_gray_original = cv2.cvtColor(self.img_original, cv2.COLOR_BGR2GRAY)
        self.img_horizontal = self.img_original
        self.img_gray_horizontal = self.img_original
        self.img_fovea_point = self.img_original
        self.img_membranes = self.img_original
        self.fovea_point = (0, 0)
        self.first_point_coroides = (0, 0)
        self.second_point_coroides = (0, 0)
        # self.micras_por_pixel = 200/33.0
        # self.micras_por_pixel = 6
        self.micras_por_pixel = 200 / 50.0
        # self.micras_por_pixel = 4.0
        self.step_one = False
        self.step_two = False
        self.step_three = False

    def to_horizontal(self):
        self.step_one = True
        # img_hough = im.copy()
        edges_canny = cv2.Canny(self.img_gray_original, 150, 200, apertureSize=3)
        lines = cv2.HoughLines(edges_canny, 1, numpy.pi / 180, 275)
        if lines is None:
            self.img_horizontal = self.img_original
        else:
            # http://homepages.inf.ed.ac.uk/rbf/HIPR2/hough.htm
            # http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
            # https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/houghlines.py
            for rho, theta in lines[0]:
                # a = np.cos(theta)
                # b = np.sin(theta)
                # x0 = a * rho
                # y0 = b * rho
                # Here i have used int() instead of rounding the decimal value, so 3.8 --> 3
                # But if you want to round the number, then use np.around() function, then 3.8 --> 4.0
                # But we need integers, so use int() function after that, ie int(np.around(x))
                # x1 = int(x0 + 1000 * (-b))
                # y1 = int(y0 + 1000 * (a))
                # x2 = int(x0 - 1000 * (-b))
                # y2 = int(y0 - 1000 * (a))
                # cv2.line(img_hough, (x1, y1), (x2, y2), (0, 255, 0), 5)

                # Use the first not horizontal line as reference and rotate with that theta

                # radians to degrees (precision float error allowed < 1)
                # theta > 0 avoid vertical lines
                if abs((theta * 180 / numpy.pi) - 90) > 1 and theta > 0:  # 90 degrees line is horizontal, not use as reference
                    # print "theta = %s\n" % (theta * 180 / numpy.pi)
                    # http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
                    rows, cols = self.img_gray_original.shape
                    # rotate image to the horizontal (line of reference degrees minus 90 degrees)
                    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), (theta * 180 / numpy.pi) - 90, 1)
                    self.img_horizontal = cv2.warpAffine(self.img_original, M, (cols, rows))
                    if self.img_horizontal is None:
                        self.img_horizontal = self.img_original
                    break
        self.img_gray_horizontal = cv2.cvtColor(self.img_horizontal, cv2.COLOR_BGR2GRAY)

    def calculate_fovea(self):
        self.step_two = True
        # ret, otsu_threshold = cv2.threshold(self.img_gray_horizontal, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blur = cv2.medianBlur(self.img_gray_horizontal, 7)
        ret, binary_threshold = cv2.threshold(blur, 30, 255, cv2.THRESH_BINARY)
        # cv2.imwrite(os.path.splitext(self.image_name)[0] + '_' + 'thresh' + os.path.splitext(self.image_name)[1], otsu_threshold)
        # print otsu_threshold[0,0]
        # print otsu_threshold.shape
        # si cv2.imread(..., 0) sólo escala de grises 0..255 y (332, 1031) si no, [0..255 0..255 0..255] (332, 1031, 3)
        # y se puede dibujar con colores en la imagen 

        y, x = binary_threshold.shape

        # Hemos comprobado que el threshold en más de una ocasión crea una línea recta horizontal en la fóvea.
        # Para encontrar un punto céntrico,
        # llevaremos dos puntos de coordenadas, el de más a la izquierda y el de más a la derecha,
        # para así luego poder calcular la media en el eje x
        punto1 = (0, 0)
        punto2 = (0, 0)

        # Restringimos el área para buscar en el eje de las x
        # teniendo en cuenta que la fóvea esta siempre entre 1/3 y 2/3
        for i in xrange(x / 3, 2 * x / 3):
            for j in xrange(y):

                if binary_threshold[j, i] == 255:

                    # Actualización punto más bajo y a la derecha
                    if punto1[1] == j:
                        punto2 = (i, j)

                    # Actualización de los puntosq más bajos
                    if punto1[1] < j:
                        punto1 = (i, j)
                        punto2 = (i, j)

                    break

                    # Cálculo de la media de los valores de la x de los dos puntos
        x = (punto1[0] + punto2[0]) / 2
        y = punto1[1]

        self.img_fovea_point = self.img_horizontal.copy()
        self.fovea_point = (x, y)
        # cv2.circle(self.img_fovea_point, punto1, 2, (0, 255, 0), 3)  # draw the center of the circle
        cv2.circle(self.img_fovea_point, self.fovea_point, 2, (0, 0, 255), 3)  # draw the center of the circle
        # cv2.circle(self.img_fovea_point, punto2, 2, (0, 255, 0), 3)  # draw the center of the circle
        # cv2.line(self.img_fovea_point, self.fovea_point, (self.fovea_point[0], self.img_fovea_point.shape[0]),
        # (255, 0, 0), 1)

    def membranes_detector(self):
        self.step_three = True
        self.img_membranes = self.img_horizontal.copy()

        ret, img_first_point = cv2.threshold(self.img_gray_horizontal, 179, 255, cv2.THRESH_BINARY)

        img_first_point = cv2.Canny(img_first_point, 100, 100 * 3, apertureSize=3)
        # cv2.imshow('img_first_point', img_first_point)

        for i in xrange(3 * img_first_point.shape[0] / 4, self.fovea_point[1], -1):
            if img_first_point[i, self.fovea_point[0]] == 255:
                if self.first_point_coroides[1] == 0:
                    self.first_point_coroides = (self.fovea_point[0], i)

        img_second_point = cv2.medianBlur(self.img_gray_horizontal, 13)
        adaptative_threshold = cv2.adaptiveThreshold(img_second_point, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 173, 3)
        # cv2.imshow('img_second_point', img_second_point)

        # Generamos nuestro propio canny a partir de findcontours y quitar los más pequeños, el ruido
        contours, hierarchy = cv2.findContours(adaptative_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        final_contours = []
        for contour in contours:
            if cv2.contourArea(contour) > 4000.0:
                final_contours.append(contour)

        # http://stackoverflow.com/a/12890573
        black_img = numpy.zeros((self.img_membranes.shape[0], self.img_membranes.shape[1], 3), numpy.uint8)
        cv2.drawContours(black_img, final_contours, -1, (255, 255, 255), 1)
        cv2.line(black_img, (0, 6*black_img.shape[0]/7), (black_img.shape[1] - 1, 6*black_img.shape[0]/7), (0, 255, 0), 1)
        img_second_point = cv2.cvtColor(black_img, cv2.COLOR_BGR2GRAY)
        # img_second_point_canny = cv2.Canny(adaptative_threshold, 50, 50 * 5, apertureSize=5)
        # cv2.imwrite(os.path.splitext(self.image_name)[0] + '_' + 'img_second_point_canny' + os.path.splitext(self.image_name)[1], img_second_point_canny)
        # cv2.imwrite(os.path.splitext(self.image_name)[0] + '_' + 'img_second_point' + os.path.splitext(self.image_name)[1], img_second_point)
        # cv2.imshow('img_second_point', img_second_point)

        # detectar el punto inferior de arriba a abajo
        # second = 0
        # for i in xrange(self.first_point_coroides[1], img_second_point.shape[0], 1):
        #     if img_second_point[i, self.fovea_point[0]] == 255:
        #         self.second_point_coroides = (self.fovea_point[0], i)
        #         second += 1
        #         if second == 2:
        #             break

        # detectar el punto inferior de abajo a arriba
        for i in xrange(6 * img_second_point.shape[0] / 7, self.first_point_coroides[1], -1):
            if img_second_point[i, self.fovea_point[0]] == 255:
                if self.second_point_coroides[1] == 0:
                    self.second_point_coroides = (self.fovea_point[0], i)

        # cv2.circle(self.img_membranes, self.first_point_coroides, 2, (0, 0, 255), 3)
        # cv2.circle(self.img_membranes, self.second_point_coroides, 2, (0, 0, 255), 3)
        cv2.line(self.img_membranes, (self.first_point_coroides[0], self.first_point_coroides[1]),
                 (self.second_point_coroides[0], self.second_point_coroides[1]), (0, 255, 0), 1)
        cv2.line(self.img_membranes, (self.first_point_coroides[0] - 15, self.first_point_coroides[1]),
                 (self.first_point_coroides[0] + 15, self.first_point_coroides[1]), (0, 0, 255), 1)
        cv2.line(self.img_membranes, (self.second_point_coroides[0] - 10, self.second_point_coroides[1]),
                 (self.second_point_coroides[0] + 10, self.second_point_coroides[1]), (0, 0, 255), 1)

        micras = (self.second_point_coroides[1] - self.first_point_coroides[1]) * self.micras_por_pixel
        p = (self.first_point_coroides[0] + 50, (self.first_point_coroides[1] + self.second_point_coroides[1]) / 2)
        cv2.putText(self.img_membranes, str(micras), p, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 1, cv2.CV_AA)

    def show_step(self, number):
        img = self.img_original
        title = 'Original'
        if number == 1 and self.step_one:
            img = self.img_horizontal
            title = 'Horizontal'

        if number == 2 and self.step_two:
            img = self.img_fovea_point
            title = 'FoveaPoint'

        if number == 3 and self.step_three:
            img = self.img_membranes
            title = 'Membranes'
        cv2.imwrite(os.path.splitext(self.image_name)[0] + '_' + title + os.path.splitext(self.image_name)[1], img)
        cv2.imshow(title, img)


def run_algorithm(img_name):

    algorithm = Algorithm(img_name)
    # algorithm.show_step(0)
    algorithm.to_horizontal()
    # algorithm.show_step(1)
    algorithm.calculate_fovea()
    # algorithm.show_step(2)
    algorithm.membranes_detector()
    algorithm.show_step(3)


if __name__ == "__main__":

    args_processor.carpeta_procesada = 'PROCESADAS'
    args_processor.args = args_processor.parser.parse_args()

    start = cv2.getTickCount()
    if args_processor.args.pasos:
        pass

    if args_processor.args.archivos:
        for archivo in args_processor.args.archivos:
            args_processor.procesar_archivo(archivo, args_processor.carpeta_procesada, run_algorithm)

    if args_processor.args.carpetas:
        for carpeta in args_processor.args.carpetas:
            os.chdir(carpeta)
            args_processor.procesar_carpeta(args_processor.carpeta_procesada, run_algorithm)
            os.chdir('..')

    end = cv2.getTickCount()
    seconds = (end - start) / cv2.getTickFrequency()
    print 'seconds elapsed: ', seconds

    cv2.waitKey(0) & 0xFF  # 64 bits
    cv2.destroyAllWindows()

