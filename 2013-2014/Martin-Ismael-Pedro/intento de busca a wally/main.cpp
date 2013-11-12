

#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include "buscaobjetos.h"



using namespace cv;
using namespace std;





int main(){
   
    Mat img,trozo ;
    img = imread( "/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/scene1.jpg");
    trozo = imread( "/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/waldo.jpg" );
    
    Buscaobjetos b(img,trozo);
    b.deteccion();
    b.mostrar();
    
}
