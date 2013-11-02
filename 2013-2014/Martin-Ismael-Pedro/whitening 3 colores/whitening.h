//
//  whitening.h
//  proyectoprimeroopencv
//
//  Created by Pedro pablo Perea de dueñas on 01/11/13.
//  Copyright (c) 2013 Pedro pablo Perea de dueñas. All rights reserved.
//

#ifndef __proyectoprimeroopencv__whitening__
#define __proyectoprimeroopencv__whitening__

#include <iostream>
#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>

using namespace cv;

class Whitening{
private:
    Mat img;
public:
    Whitening(Mat imagen){
        this->img=imagen;
    }
    void mostrar(){
        namedWindow("Whitening");
        imshow("Whitening", this->img);
    }
    
    double mediaR(){
        int resultado=0;
        for(int i=0;i<img.rows;i++){
         for(int j=0;j<img.cols;j++){
             Vec3b& rgb = img.at<Vec3b>(i,j);
             resultado=resultado + rgb[2];
         }
         }
        return resultado/(img.rows * img.cols);
        
    }
    double mediaG(){
        double resultado=0;
        for(int i=0;i<img.rows;i++){
            for(int j=0;j<img.cols;j++){
                Vec3b& rgb = img.at<Vec3b>(i,j);
                resultado=resultado + rgb[1];
            }
        }
        return  (resultado/(img.rows * img.cols));
        
    }
    double mediaB(){
        double resultado=0;
        for(int i=0;i<img.rows;i++){
            for(int j=0;j<img.cols;j++){
                Vec3b& rgb = img.at<Vec3b>(i,j);
                resultado=resultado + rgb[0];
            }
        }
        return resultado/(img.rows * img.cols);
        
    }
   
   
    double desviacionR(){
        double resultado=0;
        double cuadrado=0;
        double resta;
        double mediaR=this->mediaR();
        for(int i=0;i<img.rows;i++){
            for(int j=0;j<img.cols;j++){
                Vec3b& rgb = img.at<Vec3b>(i,j);
                resta= rgb[2] - mediaR;
                cuadrado=pow(resta,2);
                resultado=resultado + cuadrado;
            }
        }
        resultado= resultado/(img.cols * img.rows);
        resultado=sqrt(resultado);
        return resultado;
    }
    double desviacionG(){
        double resultado=0;
        double cuadrado=0;
        double resta;
        double mediaG=this->mediaG();
        for(int i=0;i<img.rows;i++){
            for(int j=0;j<img.cols;j++){
                Vec3b& rgb = img.at<Vec3b>(i,j);
                resta= rgb[1] - mediaG;
                cuadrado=pow(resta,2);
                resultado=resultado + cuadrado;
            }
        }
        resultado= resultado/(img.cols * img.rows);
        resultado=sqrt(resultado);
        return resultado;
    }
    double desviacionB(){
        double resultado=0;
        double cuadrado=0;
        double resta;
        double mediaB=this->mediaB();
        for(int i=0;i<img.rows;i++){
            for(int j=0;j<img.cols;j++){
                Vec3b& rgb = img.at<Vec3b>(i,j);
                resta= abs(rgb[0] - mediaB);
                cuadrado=pow(resta,2);
                resultado=resultado + cuadrado;
                std::cout<<(int)resta << "\n";
            }
        }
        resultado= resultado/(img.cols * img.rows);
        resultado=sqrt(resultado);
        return resultado;
    }

    void whitening(){
        
        double mediaR=this->mediaR();
        double mediaG=this->mediaG();
        double mediaB=this->mediaB();
        
        
        double desviacionR=this->desviacionR();
        double desviacionG=this->desviacionG();
        double desviacionB=this->desviacionB();
        
       
        
        img=imread("/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/beach1.jpg" );
       
        Mat dst=img.clone();
        
        for(int i=0;i<img.rows;i++){
            for(int j=0;j<img.cols;j++){
                Vec3b& rgb = dst.at<Vec3b>(i,j);
              
                
                rgb[0] =(uchar)(abs(rgb[0]-mediaB)/desviacionB);
                rgb[1] =(uchar)(abs(rgb[1]-mediaG)/desviacionG);
                rgb[2] =(uchar)(abs(rgb[2]-mediaR)/desviacionR);
                
                
                
                
                
            }
        }
        this->img=dst;
        mostrar();
    }
};
#endif /* defined(__proyectoprimeroopencv__whitening__) */
