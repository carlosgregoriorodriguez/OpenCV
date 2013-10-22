#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <stdlib.h>
#include <stdio.h>

using namespace std;
using namespace cv;

/// Global variables
int threshold_value = 0;
int threshold_type = 3;
int const max_value = 255;
int const max_type = 4;
int const max_BINARY_value = 255;

Mat img1,img2,img1grey,img2grey,img3,img4;

String trackbar_type = "Type: \n 0: Binary \n 1: Binary Inverted \n 2: Truncate \n 3: To Zero \n 4: To Zero Inverted";
String trackbar_value = "Value";

/// Function headers
void Threshold( int, void* );



///MAIN
int main( int argc, char **argv ) {

    img1 = imread("/home/ruben/OpenCV/Differences/images/beach1.jpg",CV_LOAD_IMAGE_COLOR);
    img2 = imread("/home/ruben/OpenCV/Differences/images/beach2.jpg",CV_LOAD_IMAGE_COLOR);

    img1grey = imread("/home/ruben/OpenCV/Differences/images/beach1.jpg",0);
    img2grey = imread("/home/ruben/OpenCV/Differences/images/beach2.jpg",0);
    // zero as the 2nd parameter to imread means the image is loaded as grayscale image

    //Calculates the per-element absolute difference between two arrays
    absdiff(img1,img2,img3);

    // Create a window to display results
    namedWindow( "Threshold", CV_WINDOW_AUTOSIZE );

    // Create Trackbar to choose type of Threshold
    createTrackbar( trackbar_type, "Threshold", &threshold_type, max_type, Threshold );
    createTrackbar( trackbar_value,"Threshold", &threshold_value, max_value, Threshold );

    //Shoh the images
    imshow("image1",img1);
    imshow("image2",img2);
    imshow("Differences",img3);

    // Call the function to initialize
    Threshold( 0, 0 );

    waitKey(0); //ESC
    return 0;
}


void Threshold( int, void* )
{
  /* 0: Binary
     1: Binary Inverted
     2: Threshold Truncated
     3: Threshold to Zero
     4: Threshold to Zero Inverted
   */

  threshold( img3, img4, threshold_value, max_BINARY_value,threshold_type );
  imshow( "Threshold", img4 );
}

