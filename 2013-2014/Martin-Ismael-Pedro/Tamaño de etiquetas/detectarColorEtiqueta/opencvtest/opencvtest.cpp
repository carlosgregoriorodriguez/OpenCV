/*#include "stdafx.h"
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
	string filename = "multimedia/video/futurama.mkv";
    VideoCapture capture(filename);
    Mat frame;
	const int alpha_slider_max = 100;
	int alpha_slider = 1;
	double alpha;
	double beta;
	Mat blur;
	string tb;
	int tbPos;
			
			tb = "tb1";

    if( !capture.isOpened() )
        throw "Error when reading steam_avi";

    namedWindow( "video", 1);

	createTrackbar(tb, "video", &alpha_slider, alpha_slider_max, dummy);
    for( ; ; )
    {
        capture >> frame;
        //imshow("video", frame);
		blur = frame.clone();
        waitKey(20); // waits to display frame
		tbPos = getTrackbarPos(tb, "video");
		if (tbPos <= 0)
			tbPos = 1;
		cv::blur(frame, blur, Size(tbPos, tbPos), Point(-1, -1), BORDER_DEFAULT);
		imshow("video", blur);
    }
    waitKey(0); // key press to close window
    // releases and window destroy are automatic in C++ interfacev
}
void dummy(int, void *) {
	
}*/