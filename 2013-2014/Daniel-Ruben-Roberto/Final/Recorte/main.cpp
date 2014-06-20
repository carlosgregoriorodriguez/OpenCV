#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <math.h>

using namespace std;
using namespace cv;

bool leftDown = false;
bool leftUp = false;
Mat img; //Imagen original

//----Crop
Mat croppedImage; //Imagen recortada
Point cornerLeftUp, cornerRightDown; //Inicio y finalización de la selección del usuario
Rect box; //(ROI)Regions of Interest

static void mouse_callback(int event, int x, int y, int, void*);

int main() {
    // Leer imagen
    //img = imread("../Heridas/Foto14-03-14_10_21_39.jpg");
    img = imread("../images/IMG_3985.jpg");
    resize(img, img, Size(img.cols / 4.5, img.rows / 4.5));
    
    imshow("Aplicacion de recorte", img);

    setMouseCallback("Aplicacion de recorte", mouse_callback);

    //Wait spaceBar
    while(waitKey(1) != 32);

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
        imwrite("../cropeadas/IMG_3985.jpg", croppedImage);

        leftDown = false;
        leftUp = false;
    }
}