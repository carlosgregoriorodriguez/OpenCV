/* 
 * File:   main.cpp
 * Author: Daniel
 *
 * Created on 15 de diciembre de 2013, 18:47
 */

#include <cstdlib>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"


using namespace std;
using namespace cv;

/*
 * 
 */
int main(int argc, char** argv) {
    
    Mat blur, img, img_od, final, eq, img_dst, centers, canny, dst;
    int K = 8;
    int height, width, step, channels;
    //uchar* data;
    
    
    
    img = imread("img/img1.jpg");
    
    //ALGORITMO PARA AUMENTAR LAS DIFERENCIAS DE COLORES EN UNA MISMA FOTO Y MEJORAR EL COLOR
    cvtColor(img, img, CV_BGR2GRAY);
    resize(img, img, (Size(612,384)));
    
    equalizeHist(img, eq);
    cvtColor(eq, eq, CV_GRAY2BGR);
    
    //FIN DEL ALGORITMO
    
    //eq por img
    imshow("Original", eq);
    //eq por img
    
    
    //ALGORITMO DE DETECCIÓN DE PIEL SANA
    img_od = eq.reshape(img.depth(),img.rows*img.cols);
    img_od.convertTo(img_od, CV_32F, 1./255);
    //imshow("IMG_OD", img_od);
    /*
     * Con K = 8 y epsilon 0.5 resultado interesante para las img1 e img2
     * Para la img5 hace falta, de momento, 1.15 de epsilon
     */
    kmeans(img_od,K
            ,img_dst,TermCriteria( CV_TERMCRIT_EPS+CV_TERMCRIT_ITER, 10, 0.5),3, KMEANS_PP_CENTERS, centers);
    //Mat final = img_dst;
    final = img_dst.reshape(img.depth(), img.rows);
    //canny(final, final, threshold1, threshold2);

        //We proceed to invert the "final" image.
    height = final.rows;
    width = final.cols;
    
    //Step es el tamaño de cada fila.
    //step = final.step;
    channels = final.depth();
    
    //Data es un array enorme cuya longitud es height*width
    //data = final.data;

    final.convertTo(final, 16, 255.);
    
    //FIN DEL ALGORITMO
    //imshow("final1", final);
    //waitKey();
    //cout << final.at<int>(5,5);
    threshold(final, dst, 0, 255, THRESH_BINARY);
    
    
    //Invertir la imagen para sacar las cosas malas
    
    
    imshow("threshold", dst);
    waitKey();
    //GaussianBlur(final, blur, Size(0,0), 4);
    //imshow("GaussianBlur", blur);
    
    //Canny(blur, canny, 10, 15);
    //imshow("Canny", canny);
    
    double alpha, beta;
    alpha = 0.5;
    beta = (1.0 - alpha);
    //addWeighted(img, alpha, canny, beta, 0.0, dst);
    //cvtColor(final,final,CV_YUV2BGR);
    //imshow("Resultado", canny);
    //waitKey();
    //cvReleaseImage(&final );
    //delete data;
    return 0;
}

