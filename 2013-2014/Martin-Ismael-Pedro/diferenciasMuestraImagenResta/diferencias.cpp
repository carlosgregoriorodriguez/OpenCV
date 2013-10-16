#include "stdafx.h"
#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

void dummy(int, void *);

int main( int argc, char** argv )
{
	//Vars
	Mat image1,image2;

	//Read both images
	image1 = imread("image1.jpg", CV_LOAD_IMAGE_COLOR);
	image2 = imread("image2.jpg", CV_LOAD_IMAGE_COLOR);
    
    //show images
    namedWindow("IMAGEN1", CV_WINDOW_AUTOSIZE );//name of window
    namedWindow("IMAGEN2", CV_WINDOW_AUTOSIZE );
    imshow("IMAGEN1", image1);//show the window
    cvMoveWindow( "IMAGEN1",  100,100  );
    imshow("IMAGEN2", image2);
    cvMoveWindow( "IMAGEN2", 700, 100 );
    
	// Check for invalid input
	if(!image1.data || !image2.data )
	{
		cout <<  "Could not open or find the image" << std::endl ;
		return -1;
	}

	//Get the diference
	MatExpr c = abs(image1-image2);

	//Create the window
	namedWindow("Display window", CV_WINDOW_AUTOSIZE );// Create a window for display.

	//Show the image
	imshow("Display window", c);

	//Wait
	waitKey(0);
    
    //destroy
    cvDestroyAllWindows();
}