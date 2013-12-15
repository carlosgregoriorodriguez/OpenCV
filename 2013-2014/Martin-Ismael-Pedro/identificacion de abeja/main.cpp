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

void dummy(int, void *);
void readme();
Point followInterestPoint(Mat image, Mat tpl, Point interestPoint, int squareSize);
Point detectInterestPointFromTemplate (Mat tpl);
void on_trackbar(int valor,void*);
void initialize();
int openVideo(int argc, string videoPath);
void changeColorRepresentation();
void moveDetection();

int main( int argc, char** argv )
{
	int select;
	string numWasp = "";
	int idSize = 25;

	cout << "Insert numeric code for wasp detection method: " << endl;
	cout << "1: Change color representation of images (BGR to HSV)." << endl;
	cout << "2: Movement detection among video frames" << endl;
	cout << "3: Follow wasp." << endl;
	cin >> select;
	switch(select) {
		case 1: {
			changeColorRepresentation();
		}	
		break;
		case 2: {
			moveDetection();
		}
		case 3: {
			cout << "Introduce the number of the wasp to be followed: " << endl;
			cin >> numWasp;
			
			Mat tpl;
			
			Point followedPoint = Point(-1, -1);

			int squareSize = 100;
			
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
			cout << "first";
			for(;;)
			{
				waitKey(20);
				if (frame.data) {
					previousFrame = frame.clone();
				}
				cap >> frame;
				resize(frame, frame, Size(700, 550), 0, 0, INTER_CUBIC);
				if(!frame.data)
				{
					printf("Error: no frame data.\n");
					break;
				}
				
				tbPos = getTrackbarPos(tb, "video");

				if (tbPos <= 0)
					tbPos = 1;

				tpl = imread("multimedia/images/" + numWasp + ".jpg", CV_32FC1);
				// scene1 is the captured image from the video.
				if (followedPoint.x < 0 || followedPoint.y < 0) {
					followedPoint = detectInterestPointFromTemplate(tpl);
				}
				else {
					followedPoint = followInterestPoint(frame, tpl, followedPoint, squareSize);
				}
				if (followedPoint.x >= 0 && followedPoint.y >= 0) {
					circle(frame, followedPoint, idSize, Scalar(0,255,0), 2, 8, 0);
				}
				imshow("video", frame);
			}
		}
		break;
		default:
		break;
	}
	
    return 0;
	
}

Point followInterestPoint(Mat image, Mat tpl, Point interestPoint, int squareSize) {
	Mat scores;
	Point minLoc; 
	Point maxLoc;
	Point foundPoint;
	double minVal; 
	double maxVal; 
	int initX, initY, squareX, squareY;
	cout << interestPoint.x << " " << interestPoint.y << endl;
	if (interestPoint.y - squareSize/2 < 0)
		initX = 0;
	else {
		initX = interestPoint.y - squareSize/2;
	}
	if (interestPoint.x - squareSize/2 < 0)
		initY = 0;
	else {
		initY = interestPoint.x - squareSize/2;
	}
	if (initX + squareSize/2 >= image.rows)
		squareX = image.rows - 1;
	else {
		squareX = squareSize;
	}
	if (initY + squareSize >= image.cols)
		squareY = image.cols - 1;
	else {
		squareY = squareSize;
	}
	cout << image.rows << " " << image.cols << endl;
	cout << initX << " " << initY << " " << squareX << " " << squareY;
	cout << "hola1 " << endl;
	Mat subImg = image(Rect(initY, initX, squareX, squareY));
	cout << "hola2 " << endl;
	scores.create(tpl.rows, tpl.cols, CV_32FC1);
	cout << "hola3 " << endl;
	matchTemplate(subImg, tpl, scores, TM_CCORR_NORMED);
	//normalize( scores, scores, 0, 1, NORM_MINMAX, -1, Mat() );
	 /// Localizing the best match with minMaxLoc
	 cout << "hola4 " << endl;
	minMaxLoc( scores, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );
	cout << "hola5 " << endl;
	foundPoint = Point(maxLoc.x + interestPoint.x - squareSize/2, 
		maxLoc.y + interestPoint.y - squareSize/2);
	cout << "hello " <<foundPoint.x << " " << foundPoint.y << endl;
	
	return foundPoint;
}

Point detectInterestPointFromTemplate (Mat tpl) {
	Mat scores;
	Point minLoc; 
	Point maxLoc;
	double minVal; 
	double maxVal; 
	
	scores.create(tpl.rows, tpl.cols, CV_32FC1);
	
	matchTemplate(frame, tpl, scores, TM_CCORR_NORMED);
	//normalize( scores, scores, 0, 1, NORM_MINMAX, -1, Mat() );
	 /// Localizing the best match with minMaxLoc
	minMaxLoc( scores, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );
		
	return maxLoc;
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