#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <math.h>
#include <stdio.h>
#include <iostream>

using namespace cv;
using namespace std;

//----Crop
bool leftDown = false;
bool leftUp = false;
Mat img; //Imagen original

Mat croppedImage; //Imagen recortada
Point cornerLeftUp, cornerRightDown; //Inicio y finalización de la selección del usuario
Rect box; //(ROI)Regions of Interest

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
static void mouse_callback(int event, int x, int y, int, void*);

//Posibles valores
// 4,41,69,75
// 3,49,27,76
// 3,37,100,70

// Main
int main(int argc, char** argv) {
    //img = imread("../QUEMADOS/mdcg2695150/20130319/IMG_3981_1500x1000.JPG", 1);
    //img = imread("../QUEMADOS/mpm2673522/27marzo2013/IMG_3997.JPG", 1);
    //img = imread("../images/new.jpg", 1);
    
    //Recorte
    img = imread("../images/IMG_3985.jpg");
    resize(img, img, Size(img.cols / 4.5, img.rows / 4.5));
    imshow("Aplicacion de recorte", img);
    setMouseCallback("Aplicacion de recorte", mouse_callback);
    //Wait spaceBar
    while(waitKey(1) != 32);
    
    //Gabor filters
    Mat image_grey;
    cvtColor(croppedImage, image_grey, CV_BGR2GRAY); //Convertir a escala de grises
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

// Callback para los eventos de ratón
static void mouse_callback(int event, int x, int y, int, void*) {
    //Botón izquierdo del ratón presionado
    if (event == EVENT_LBUTTONDOWN) {
        leftDown = true;
        cornerLeftUp.x = x;
        cornerLeftUp.y = y;
    }
    
    //Botón izquierdo del ratón soltado
    if (event == EVENT_LBUTTONUP) {
        //Si la selección > 20 px
        if (abs(x - cornerLeftUp.x) > 20 && abs(y - cornerLeftUp.y) > 20) {
            leftUp = true;
            cornerRightDown.x = x;
            cornerRightDown.y = y;
        } else {
            cout << "Seleccione una región más grande" << endl;
            leftDown = false;
        }
    }
    
    // Actualizar el rectángulo
    if (leftDown == true && leftUp == false) {
        Point pt;
        pt.x = x;
        pt.y = y;
        Mat local_img = img.clone();
        rectangle(local_img, cornerLeftUp, pt, Scalar(0, 0, 255));
        imshow("Aplicacion de recorte", local_img);
    }
    
    // Recortar cuando ambas esquinas han sido seleccionadas
    if (leftDown == true && leftUp == true) {
        box.width = abs(cornerLeftUp.x - cornerRightDown.x);
        box.height = abs(cornerLeftUp.y - cornerRightDown.y);
        box.x = min(cornerLeftUp.x, cornerRightDown.x);
        box.y = min(cornerLeftUp.y, cornerRightDown.y);

        Mat crop(img, box);
        imshow("Recorte", crop);

        // Clonar y guardar imagen
        croppedImage = img(box).clone();
        //imwrite("../cropeadas/IMG_3985.jpg", croppedImage);

        leftDown = false;
        leftUp = false;
    }
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