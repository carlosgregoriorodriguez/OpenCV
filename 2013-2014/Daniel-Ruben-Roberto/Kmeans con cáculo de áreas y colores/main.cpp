/* 
 * File:   main.cpp
 * Author: Daniel
 *
 * Created on 15 de diciembre de 2013, 18:47
 */

#include <cstdlib>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "heridas.h";


using namespace std;  
using namespace cv;

/*
 * 
 */
int main(int argc, char** argv) {
    preparaImagen("img/img4.jpg");
    aplicaKmeans("img/crop.jpg");
}

