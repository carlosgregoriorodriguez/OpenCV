#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <math.h>
#include <stdio.h>
#include <iostream>

using namespace cv;
using namespace std;

// Variables globales 
int kernel_size = 15;
int pos_sigma = 3; //gaussvar - Variable gaussiana
int pos_theta = 37; //orientation - Orientación
int pos_lambda = 100; //wavelength - Longitud de onda
int pos_psi = 81; //phaseoffset - Desviación de Fase
Mat image_float;
Mat image_gabor_filter;

// Encabezados
Mat makeKernel(int ksize, double sig, double th, double lm, double ps);
void GFValues(int, void *);

//Posibles valores
// 4,41,69,75
// 3,49,27,76
// 3,37,100,70

// Main
int main(int argc, char** argv) {
    //Mat image = imread("../QUEMADOS/mdcg2695150/20130319/IMG_3981_1500x1000.JPG", 1);
    //Mat image = imread("../QUEMADOS/mpm2673522/27marzo2013/IMG_3997.JPG", 1);
    //Mat image = imread("../images/new.jpg", 1);
    //Mat image = imread("../recortadas/vieja2.jpg", 1);
    Mat image = imread("../cropeadas/IMG_3985-Cropper.jpg", 1);

    //resize(image, image, Size(image.cols/5, image.rows/6));
    imshow("Original", image);
    
    Mat image_grey;
    cvtColor(image, image_grey, CV_BGR2GRAY); //Convertir a escala de grises
    image_grey.convertTo(image_float, CV_32F, 1.0/255, 0); //Convertir a tipo Float
    //Tamaño del núcleo par - máx.gaussVar
    if (!kernel_size % 2) {
        kernel_size += 1;
    }
    
    namedWindow("Gabor Filter Values", 1);
    createTrackbar("GaussVar(sig)", "Gabor Filter Values", &pos_sigma, kernel_size, GFValues);
    createTrackbar("Orientation(th)", "Gabor Filter Values", &pos_theta, 180, GFValues);
    createTrackbar("Wavelenght(lm)", "Gabor Filter Values", &pos_lambda, 100, GFValues);
    createTrackbar("PhaseOffset(psi)", "Gabor Filter Values", &pos_psi, 360, GFValues);
    GFValues(0, 0); //GaborFilter
    
    waitKey(0);
    
    //Get the last parameters
    int post_sigma = getTrackbarPos("GaussVar(sig)","Gabor Filter Values");
    int post_lambda = getTrackbarPos("Wavelenght(lm)","Gabor Filter Values");
    int post_theta = getTrackbarPos("Orientation(th)","Gabor Filter Values");
    int post_psi = getTrackbarPos("PhaseOffset(psi)","Gabor Filter Values");

    //Guardar imagen
    Mat filtered;
    Mat save;
    Mat saveKernel = makeKernel(kernel_size, post_sigma, post_theta, post_lambda, post_psi);
    filter2D(image_float, filtered, CV_32F, saveKernel);
    
    //Convertir a CV_8UC3
    filtered.convertTo(save, CV_8UC3, 255, 0);
    cvtColor(save,save,CV_GRAY2RGB);
    
    imshow("Gabor Filter Final", save);
    imwrite("../images/Gabor.jpg", save);

    waitKey(0);
    return 0;
}

//Mat getGaborKernel(Size ksize, double sigma, double theta, double lambd, double gamma, double psi=CV_PI*0.5, int ktype=CV_64F )
Mat makeKernel(int ksize, double sig, double th, double lm, double ps) {
    //gamma = 1
    int hksize = (ksize - 1) / 2;
    double theta = th * CV_PI / 180;
    double psi = ps * CV_PI / 180;
    double del = 2.0 / (ksize - 1);
    double lambda = 0.5 + lm / 100.0;
    double sigma = sig / ksize;
    double x_theta;
    double y_theta;
    Mat kernel(ksize, ksize, CV_32F);
    for (int y = -hksize; y <= hksize; y++) {
        for (int x = -hksize; x <= hksize; x++) {
            x_theta = x * del * cos(theta) + y * del * sin(theta);
            y_theta = -x * del * sin(theta) + y * del * cos(theta);
            kernel.at<float>(hksize + y, hksize + x) = (float) exp(-0.5 * (pow(x_theta, 2) + pow(y_theta, 2)) / pow(sigma, 2)) * cos(2 * CV_PI * x_theta / lambda + psi);
        }
    }
    return kernel;
}

void GFValues(int, void *) { 
    //Gabor Filter
    Mat kernel = makeKernel(kernel_size, pos_sigma, pos_theta, pos_lambda, pos_psi);
    filter2D(image_float, image_gabor_filter, CV_32F, kernel); // Aplicar filtro
    imshow("Gabor Filter Values", image_gabor_filter);
    
    //Imagen del kernel
    Mat kernelImage(kernel_size * 20, kernel_size * 20, CV_32F);
    resize(kernel, kernelImage, kernelImage.size());
    kernelImage /= 2.;
    kernelImage += 0.5;
    imshow("Kernel", kernelImage);
    
    /// Gabor Filter Values pow 2
    Mat image_gabor_filter_pow;
    pow(image_gabor_filter, 2.0, image_gabor_filter_pow);
    imshow("Gabor Filter Values^2", image_gabor_filter_pow);
}