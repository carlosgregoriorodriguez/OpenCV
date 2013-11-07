#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>

using namespace cv;
using namespace std;


int main( int argc, char** argv ) {

    Mat src, dst;

    //Windows names
    char* source_window = "Source image";
    char* equalized_window = "Equalized Image";

    /// Load source image
    src = imread("/home/ruben/OpenCV/images/botin.jpg");

    if( !src.data ) {
        cout << "Error al leer la imagen" << endl;
        return -1;
    }

    /// Convert to grayscale
    cvtColor( src, src, CV_BGR2GRAY );

    /// Apply Histogram Equalization
    // void equalizeHist(InputArray src, OutputArray dst)
    equalizeHist( src, dst );

    /// Display results
    namedWindow( source_window, CV_WINDOW_AUTOSIZE );
    namedWindow( equalized_window, CV_WINDOW_AUTOSIZE );

    imshow( source_window, src );
    imshow( equalized_window, dst );

    /// Wait until user exits the program
    waitKey(0);

    return 0;

}
