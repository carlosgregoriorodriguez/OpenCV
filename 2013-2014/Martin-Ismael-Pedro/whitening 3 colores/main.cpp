/*#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <opencv2/opencv.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <stdio.h>*/

#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include "whitening.h"

using namespace cv;
using namespace std;


int main(){
    Mat src,dst,dst1,dst2 ;
    src=imread("/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/beach1.jpg" );
    //cvtColor(src, dst, CV_BGR2GRAY);
    Whitening wh(src);
    /*src=imread("/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/botin1.jpg");
    cvtColor(src, dst, CV_8U);
    
    //Mat s=src.col(0);

    namedWindow("imagen normalizada");
    imshow("imagen normalizada", dst);
    
    */
    //double media,varianza;
    //media=wh.media();
    //varianza=wh.varianza();
    //cout<<media;
    //wh.mostrar();
    wh.whitening();
    //printf("Resultado %f",media);
    //printf("Varianza %f",varianza);
    //wh.mostrar();
    waitKey(0);
    
}