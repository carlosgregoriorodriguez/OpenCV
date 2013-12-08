#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include <stdio.h>
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/nonfree/nonfree.hpp"

using namespace cv;
using namespace std;

void dummy(int, void *);
void readme();

cv::VideoCapture cap;
int tbPos;
const int alpha_slider_max = 100;
int alpha_slider = 1;
double alpha;
double beta;
Mat frame;
Mat previousFrame;
Mat blurred;
string tb = "tb1";

void on_trackbar(int valor,void*);
void initialize();
int openVideo(int argc, string videoPath);
void changeColorRepresentation();
void moveDetection();

int main( int argc, char** argv )
{
	int select;

	cout << "Insert numeric code for wasp detection method: " << endl;
	cout << "1: Change color representation of images (BGR to HSV)." << endl;
	cout << "2: Movement detection among video frames" << endl;
	cin >> select;
	switch(select) {
		case 1: {
			changeColorRepresentation();
		}	
		break;
		case 2: {
			moveDetection();
		}
		break;
		default:
		break;
	}
	
    return 0;
	
}

void on_trackbar(int valor,void*){
	//TODO
	
}

void initialize() {
	alpha_slider = 1;
	frame = Mat();
	blurred = Mat();
	tb = "tb1";
}

int openVideo(int argc, string videoPath) {
	int error;

	if(argc > 1)
	{
		cap.open(videoPath);
	}
	else
	{
		cap.open(CV_CAP_ANY);
	}
	if(!cap.isOpened())
	{
		printf("Error: could not load a camera or video.\n");
		error = 0;
	}
	else
		error = 1;
	
	return error;
}

void changeColorRepresentation() {
	cv::Mat initialImage = cv::imread("multimedia/images/wasps.jpg");

    cv::cvtColor(initialImage, initialImage, CV_BGR2HSV);
	cv::Mat image= cv::imread("multimedia/images/wasps.jpg");
    if (!image.data) {
        std::cout << "Image file not found\n";
    }

    //Prepare the image for findContours
    cv::cvtColor(image, image, CV_BGR2GRAY);
    cv::threshold(image, image, 230, 255, CV_THRESH_BINARY);

    //Find the contours. Use the contourOutput Mat so the original image doesn't get overwritten
    std::vector<std::vector<cv::Point> > contours;
    cv::Mat contourOutput = image.clone();
    cv::findContours( contourOutput, contours, CV_RETR_TREE, CV_CHAIN_APPROX_NONE );

    //Draw the contours
    cv::Mat contourImage(image.size(), CV_8UC3, cv::Scalar(0,0,0));
    cv::Scalar colors[3];
    colors[0] = cv::Scalar(255, 0, 0);
    colors[1] = cv::Scalar(0, 255, 0);
    colors[2] = cv::Scalar(0, 0, 255);
    for (size_t idx = 0; idx < contours.size(); idx++) {
        cv::drawContours(contourImage, contours, idx, colors[idx % 3]);
    }
	cv::imshow("initial", initialImage);
    cvMoveWindow("initial", 400, 0);
    cv::imshow("Input Image", image);
    cvMoveWindow("Input Image", 0, 0);
    cv::imshow("Contours", contourImage);
    cvMoveWindow("Contours", 200, 0);
    cv::waitKey(0);
}


void moveDetection() {
	
	int error;
	
    initialize();
	/*
    if (openVideo(argc, string(argv[1])) == 0) {
		cerr << "Error: could not load a camera or video.\n";
    }
	*/
	cap.open("multimedia/video/video.mts");
	
	namedWindow("video", 1);
	
	createTrackbar(tb, "video", &alpha_slider, alpha_slider_max, on_trackbar);
	
	for(;;)
	{
		waitKey(20);
		if (frame.data) {
			previousFrame = frame.clone();
		}
		cap >> frame;
		if(!frame.data)
		{
			printf("Error: no frame data.\n");
			break;
		}
		
		tbPos = getTrackbarPos(tb, "video");

		if (tbPos <= 0)
			tbPos = 1;

		imshow("video", abs(frame-previousFrame));
	}
}