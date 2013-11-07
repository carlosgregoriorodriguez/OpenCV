///Control Limited Adaptive Histogram Equalization

#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

int clipLimit;
Mat src, dst;
int const max_value = 10;

void Clahe( int, void* );

int main( int argc, char** argv ) {

    /// Load image
    src = imread("/home/ruben/OpenCV/images/botin.jpg",CV_LOAD_IMAGE_GRAYSCALE);

    // Load the source image
    if( !src.data ) {
        cout << "Error al leer la imagen" << endl;
        return -1;
    }

    imshow("Original Gray",src);


    clipLimit = 2;
    // Create a window to display results
    namedWindow( "CLAHE", CV_WINDOW_AUTOSIZE );


    // Create Trackbar to choose
    createTrackbar( "ClipLimit", "CLAHE", &clipLimit, max_value, Clahe );

    Clahe(clipLimit, 0);


    waitKey(0);

}

void Clahe( int, void* ) {
    Ptr<CLAHE> clahe = createCLAHE();
    clahe->setClipLimit(clipLimit);
    clahe->apply(src,dst);
    imshow("CLAHE",dst);
}
