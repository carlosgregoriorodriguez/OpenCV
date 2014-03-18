#include "stdafx.h"
#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

//Variables
Mat color, color2, color3, img, mt, mt1, mt2, mt3, mt4;

//Aux Functions
void dummy(int, void *);

int main( int argc, char** argv )
{
	//Read images
	color = imread("multimedia/images/color_punta_ala_avispa.jpg", CV_32FC1);
	color3 = imread("multimedia/images/color3.jpg", CV_32FC1);
	img = imread("multimedia/images/pantallazo.jpg", CV_32FC1);

	//Use match templates
	matchTemplate(img, color, mt, CV_TM_CCORR_NORMED);
	//matchTemplate(img, color3, mt1, CV_TM_CCORR_NORMED);
	//matchTemplate(img, color, mt1, CV_TM_SQDIFF_NORMED);
	//show
	namedWindow("scene",  CV_WINDOW_AUTOSIZE);
	//namedWindow("scene1",  CV_WINDOW_AUTOSIZE);

	//cvtColor( img, img, CV_RGB2GRAY );

	//Aplicamos el threshold to zero
	//threshold( mt, mt, 10, 255, 3 );
	//threshold( mt, mt, 0.9, 255, 3 );

	imshow("scene", mt);
	//imshow("scene1", mt1);

	waitKey(0);

    return 0;
}

void dummy(int, void *) {
	
}
