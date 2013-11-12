//
//  buscaobjetos.h
//  proyectoprimeroopencv
//
//  Created by Pedro pablo Perea de dueñas on 06/11/13.
//  Copyright (c) 2013 Pedro pablo Perea de dueñas. All rights reserved.
//


#ifndef __proyectoprimeroopencv__buscaobjetos__
#define __proyectoprimeroopencv__buscaobjetos__

#include <iostream>
#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>

using namespace cv;



class Buscaobjetos{
    private:
    Mat source;
    Mat trozoabuscar;
    Mat dst;
    public:
    Buscaobjetos(Mat s,Mat t){
        this->source=s;
        this->trozoabuscar=t;
        this->dst=s;
    }
    
    void deteccion(){
        Mat result;
        //por definición la imagen resultado de matching dará lo siguientes tamaños de columbas y filas
        int result_cols =  this->source.cols - this->trozoabuscar.cols + 1;
        int result_rows = this->source.rows - this->trozoabuscar.rows + 1;
        //creamos la imagen con las filas y resultados anteriores
        result.create(result_cols, result_rows, CV_32FC1);
        //Me devolverá una imagen que indica la pronbabilidad que aparezca en una determinada zona
        matchTemplate(this->source, this->trozoabuscar, result,CV_TM_SQDIFF_NORMED );
        //me devolverá los puntos minimos y maximos de la imagen
        double valorminimo, valormaximo;
        Point puntovalorminimo, puntovalormaximo;
        //coges el punto del valor minimo que en el caso del tipo de match que hemos utilizado es el que
        //nos interesa
        minMaxLoc(result, &valorminimo, &valormaximo, &puntovalorminimo, &puntovalormaximo,Mat());
        //y pintamos un rectangulo
        rectangle( dst, puntovalorminimo, Point( puntovalorminimo.x + this->trozoabuscar.cols ,puntovalorminimo.y + this->trozoabuscar.rows ), Scalar::all(0), 2, 8, 0 );
        
    }
    void mostrar(){
        namedWindow("resultado");
        imshow("resultado", this->dst);
        waitKey(0);
    }
    

};
#endif /* defined(__proyectoprimeroopencv__buscaobjetos__) */
