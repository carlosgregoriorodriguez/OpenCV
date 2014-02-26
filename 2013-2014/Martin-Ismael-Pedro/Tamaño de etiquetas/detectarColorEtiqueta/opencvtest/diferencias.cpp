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

	// Check for invalid input
	if(!image1.data || !image2.data )
	{
		cout <<  "Could not open or find the image" << std::endl ;
		return -1;
	}

	//Get the diference
	MatExpr c = abs(image1-image2);

	/*
	Delete small areas of white pixels using morphological operations (erosion).
	Use findContours to find all contours.
	Use countNonZero or contourArea to find area of each contour.
	*/

	/*
	* 1. hacemos findCountours y eso nos devuelve un array de contornos
	* 2. Calculamos el area(o algo asi para saber el punto medio) del contorno
	* 3. Sabiendo el punto medio y el area, sacamos el radio de la circunferencia que vamos a pintar y la pinamos
	*/

	Mat canny_output;
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	Mat src; 
	Mat src_gray;
	int thresh = 100;
	int max_thresh = 255;
	RNG rng(12345);

	// Detect edges using canny
	Canny( src_gray, canny_output, thresh, thresh*2, 3 );

	findContours( canny_output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );


	//Create the window
	namedWindow("Display window", CV_WINDOW_AUTOSIZE );// Create a window for display.

	//Show the image
	imshow("Display window", c);

	//Wait
	waitKey(0); 
}