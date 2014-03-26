#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include <stdio.h>
#include <math.h>
#include "opencv2/core/core.hpp"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/nonfree/nonfree.hpp"
//#include "headers.h"

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
void initialize();
int openVideo(int argc, string videoPath);
void detectIds();
void moveDetection();

bool isGreen(Mat img[], int i, int j);
bool isRed(Mat img[], int i, int j);
bool isBlue(Mat img[], int i, int j);
bool isYellow(Mat img[], int i, int j);
bool isClearBlue(Mat img[], int i, int j);
bool isPurple(Mat img[], int i, int j);
void setGreen(Mat img[], int i, int j);
void setRed(Mat img[], int i, int j);
void setBlue(Mat img[], int i, int j);
void setYellow(Mat img[], int i, int j);
void setClearBlue(Mat img[], int i, int j);
void setPurple(Mat img[], int i, int j);
void setBlack(Mat img[], int i, int j);

void findAndSetColor(Mat image, char col, Mat &retImage);
void findGreen(Mat channel[]);
void findRed(Mat channel[]);
void findBlue(Mat channel[]);
void findYellow(Mat channel[]);
void findClearBlue(Mat channel[]);
void findPurple(Mat channel[]);
void findWingsColor(Mat channel[]);
void setColor(Mat channel[], Mat color, Mat negativeColor, int B, int G, int R);


class Wasp {
public:
	int _x;
	int _y;
	char _idColor;
	int _direction;
	int _wings;
	Wasp(int x, int y) {
		_x = x;
		_y = y;
	}
	Wasp() {}
};

// Global dynamic array which keeps the info about the Wasps to be followed.
Wasp** wasps = new Wasp*[10];


int main( int argc, char** argv )
{
	int select;
	string numWasp = "";
	int idSize = 25;

	cout << "Insert numeric code for wasp detection method: " << endl;
	cout << "1: Detect wasps' ids." << endl;

	cin >> select;
	switch(select) {
case 1: {
	detectIds();
		}	
		break;

default:
	break;
	}

	return 0;

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

void detectIds() {
	int erosionSize = 1;
	int erosionType = 2;
	int thresh = 50;
	int max_thresh = 100;
	RNG rng(12345);
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	cv::Mat initialImage = cv::imread("multimedia/images/wasps2.jpg");

	cv::Mat image;
	cv::Mat splitedImages[6];
	cv::Mat ids;
	cv::Mat test;
	/*
	0,0,255
	0,0,0->discarded (black)
	0,255,0 -
	0,255,255 -
	255,0,0 -
	255,0,255 -
	255,255,0 -
	255,255,255->discarded (white)
	*/

	initialize();
	/*
	if (openVideo(argc, string(argv[1])) == 0) {
	cerr << "Error: could not load a camera or video.\n";
	}
	*/
	cap.open("multimedia/video/video.mts");
	namedWindow("video", 1);
	namedWindow("test", 1);

	cout << "first";
	for(;;)
	{
		waitKey(20);
		if (frame.data) {
			previousFrame = frame.clone();
		}
		cap >> frame;
		initialImage = frame.clone();
		resize(frame, initialImage, Size(700, 550), 0, 0, INTER_CUBIC);
		if(!initialImage.data)
		{
			printf("Error: no frame data.\n");
			break;
		}

		findAndSetColor(initialImage, 'g', splitedImages[0]);
		findAndSetColor(initialImage, 'b', splitedImages[1]);
		findAndSetColor(initialImage, 'r', splitedImages[2]);
		findAndSetColor(initialImage, 'y', splitedImages[3]);
		findAndSetColor(initialImage, 'p', splitedImages[4]);
		findAndSetColor(initialImage, 'c', splitedImages[5]);

		ids = splitedImages[0] + splitedImages[1] + splitedImages[2] + splitedImages[3] + 
			splitedImages[4] + splitedImages[5];

		Mat element = getStructuringElement( erosionType,
			Size( 2*erosionSize + 1, 2*erosionSize+1 ),
			Point( erosionSize, erosionSize ) );

		/// Apply the erosion operation
		blur( ids, ids, Size( erosionSize*5, erosionSize*5 ), Point(-1,-1) );
		namedWindow("ids",1);
		imshow("ids",ids);

		erode( ids, ids, element );
		element = getStructuringElement( erosionType,
			Size( 10*erosionSize + 1, 10*erosionSize+1 ),
			Point( 5*erosionSize, 5*erosionSize ) );
		dilate( ids, ids, element);
		blur( ids, ids, Size( erosionSize*5, erosionSize*5 ), Point(-1,-1) );
		Mat canny;
		/// Detect edges using canny
		Canny( ids, canny, thresh, thresh*2, 3 );
		/// Find contours
		findContours( canny, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

		/// Get the moments
		vector<Moments> mu(contours.size() );
		for( int i = 0; i < contours.size(); i++ )
		{ mu[i] = moments( contours[i], false ); }

		///  Get the mass centers:
		vector<Point2f> mc( contours.size() );
		for( int i = 0; i < contours.size(); i++ )
		{ mc[i] = Point2f( mu[i].m10/mu[i].m00 , mu[i].m01/mu[i].m00 ); }

		// Here we should calculate the camera distance
		float camDist = 1;
		
		// We merge the detected nearby wasps to just one
		for( int i = 0; i < contours.size(); i++ ) {
			for (int j = 0; j < contours.size(); j++) {
				if (i != j && std::sqrt((mc[i].x - mc[j].x)*(mc[i].x - mc[j].x) + 
					(mc[i].y - mc[j].y)*(mc[i].y - mc[j].y)) < camDist * 25) {
						mc[j].operator =(Point(-100, -100));
				}
			}
			
		}

		/// Draw contours
		Mat drawing = initialImage;
		test = initialImage.clone();
		Mat channel[3];
		Mat chaTest[3];	
		int wasp = 0;
		split(ids, channel);
		split(test, chaTest);
		for( int i = 0; i < contours.size(); i++ )
		{
			if (mc[i].x > 0 && mc[i].y > 0) {
				wasps[wasp] = new Wasp(mc[i].x, mc[i].y);
				Scalar color = Scalar( (int)channel[0].at<uchar>(wasps[wasp]->_y, wasps[wasp]->_x), 
					(int)channel[1].at<uchar>(wasps[wasp]->_y, wasps[wasp]->_x), 
					(int)channel[2].at<uchar>(wasps[wasp]->_y, wasps[wasp]->_x));
				//Scalar color = ids.at<uchar>(Point(mc[i].x, mc[i].y));
				//drawContours( drawing, contours, i, color, 2, 8, hierarchy, 0, Point() );
				circle( drawing, Point(wasps[wasp]->_x, wasps[wasp]->_y), 4, color, -1, 8, 0 );
				wasp++;
			}
		}

		findWingsColor(chaTest);
		merge(chaTest, 3, test);
		element = getStructuringElement( 1,
                        Size( 2*0.5 + 1, 2*0.5+1 ),
                        Point( 1, 1 ) );

                /// Apply the erosion operation
                erode( test, test, element );

		//erode(test, test, Mat(), Point(-1, -1), 2, 1, 1);

		imshow("video", drawing);
		imshow("test", test);
	}
	cv::waitKey(0);



	/*
	while(1)
	{
	//Thresholding the image
	//cv:inRange(initialImage, Scalar(h1, s1, v1), Scalar(h2,s2,v2),image);
	//Showing the images
	blur( image, image, Size( 2, 2 ), Point(-1,-1) );
	Mat element = getStructuringElement( 2,
	Size( 2*er + 1, 2*er+1 ),
	Point( er, er ) );
	erode( image, image, element );
	dilate( image, image, element );

	cv::imshow("img", image);

	/// Apply the erosion operation

	//Escape Sequence
	char c=cvWaitKey(33);
	if(c==27)
	break;
	}
	*/
	//channel[0]=Mat::zeros(initialImage.rows, initialImage.cols, CV_8UC1);
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


bool isGreen(Mat img[], int i, int j) {
	return img[0].at<uchar>(Point(j, i)) + img[2].at<uchar>(Point(j, i)) < 
		img[1].at<uchar>(Point(j, i))+50 && img[1].at<uchar>(Point(j, i)) > 140;
}

bool isRed(Mat img[], int i, int j) {
	return img[0].at<uchar>(Point(j, i))+ img[1].at<uchar>(Point(j, i)) < 
		img[2].at<uchar>(Point(j, i))+30  && img[2].at<uchar>(Point(j, i)) > 140;
}

bool isBlue(Mat img[], int i, int j) {
	return img[1].at<uchar>(Point(j, i)) + img[2].at<uchar>(Point(j, i)) < 
		img[0].at<uchar>(Point(j, i))+50 && img[0].at<uchar>(Point(j, i)) > 140;
}

bool isYellow(Mat img[], int i, int j) {
	return (img[1].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) > -20 &&
		img[1].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) < 20) &&
		img[2].at<uchar>(Point(j, i)) > 140 &&
		img[0].at<uchar>(Point(j, i)) < img[2].at<uchar>(Point(j, i))/2;
}

bool isClearBlue(Mat img[], int i, int j) {
	return (img[1].at<uchar>(Point(j, i)) - img[0].at<uchar>(Point(j, i)) > -20 &&
		img[1].at<uchar>(Point(j, i)) - img[0].at<uchar>(Point(j, i)) < 20) &&
		img[1].at<uchar>(Point(j, i)) > 140 &&
		img[2].at<uchar>(Point(j, i)) < img[1].at<uchar>(Point(j, i))/2;
}

bool isPurple(Mat img[], int i, int j) {
	return (img[0].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) > -20 &&
		img[0].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) < 20) &&
		img[0].at<uchar>(Point(j, i)) > 140 &&
		img[1].at<uchar>(Point(j, i)) < img[0].at<uchar>(Point(j, i))/2;
}

void setGreen(Mat img[], int i, int j) {
	img[0].at<uchar>(Point(j, i)) = 90;
	img[1].at<uchar>(Point(j, i)) = 200;
	img[2].at<uchar>(Point(j, i)) = 90;
}

void setRed(Mat img[], int i, int j) {
	img[0].at<uchar>(Point(j, i)) = 90;
	img[1].at<uchar>(Point(j, i)) = 90;
	img[2].at<uchar>(Point(j, i)) = 200;
}

void setBlue(Mat img[], int i, int j) {
	img[0].at<uchar>(Point(j, i)) = 200;
	img[1].at<uchar>(Point(j, i)) = 90;
	img[2].at<uchar>(Point(j, i)) = 90;
}

void setYellow(Mat img[], int i, int j) {
	img[0].at<uchar>(Point(j, i)) = 30;
	img[1].at<uchar>(Point(j, i)) = 240;
	img[2].at<uchar>(Point(j, i)) = 240;
}

void setClearBlue(Mat img[], int i, int j) {
	img[0].at<uchar>(Point(j, i)) = 240;
	img[1].at<uchar>(Point(j, i)) = 240;
	img[2].at<uchar>(Point(j, i)) = 30;
}

void setPurple(Mat img[], int i, int j) {
	img[0].at<uchar>(Point(j, i)) = 240;
	img[1].at<uchar>(Point(j, i)) = 30;
	img[2].at<uchar>(Point(j, i)) = 240;
}

void setBlack(Mat img[], int i, int j) {
	img[0].at<uchar>(Point(j, i)) = 0;
	img[1].at<uchar>(Point(j, i)) = 0;
	img[2].at<uchar>(Point(j, i)) = 0;
}

void findAndSetColor(Mat image, char col, Mat &retImage) {
	cv::Mat channel[3];
	channel[0] = Mat::zeros(image.rows, image.cols, CV_BGR2GRAY);
	channel[1] = Mat::zeros(image.rows, image.cols, CV_BGR2GRAY);
	channel[2] = Mat::zeros(image.rows, image.cols, CV_BGR2GRAY);

	split(image, channel);

	switch (col) {
	case 'g':
		findGreen(channel);
		break;
	case 'r':
		findRed(channel);
		break;
	case 'b':
		findBlue(channel);
		break;
	case 'y':
		findYellow(channel);
		break;
	case 'p':
		findPurple(channel);
		break;
	case 'c':
		findClearBlue(channel);
		break;
	}

	merge(channel, 3, retImage);

	//channel[1].setTo(cv::Mat(channel[0].rows, channel[0].cols, CV_8UC1, 200) ,color);
	//channel[2].setTo(cv::Mat(channel[0].rows, channel[0].cols, CV_8UC1, 90) ,color);

	//threshold( color, color, 1, 255, 2 );


}

void findGreen(Mat channel[]) {
	Mat color;
	Mat color1;
	color = channel[0] + channel[2];
	color1 = cv::Mat(channel[0].rows, channel[0].cols, CV_8UC1, 140);
	cv::compare(channel[1], color1, color1, CMP_GT);
	cv::compare(color, channel[1] + 50, color, CMP_LT);

	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_not(color, color1);

	setColor(channel, color, color1, 90, 200, 90);
}

void findRed(Mat channel[]) {
	Mat color;
	Mat color1;
	color = channel[0] + channel[1];
	color1 = cv::Mat(channel[2].rows, channel[2].cols, CV_8UC1, 140);
	cv::compare(channel[2], color1, color1, CMP_GT);
	cv::compare(color, channel[2] + 30, color, CMP_LT);
	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_not(color, color1);

	setColor(channel, color, color1, 90, 90, 200);
}

void findBlue(Mat channel[]) {
	Mat color;
	Mat color1;
	color = channel[1] + channel[2];
	color1 = cv::Mat(channel[0].rows, channel[2].cols, CV_8UC1, 140);
	cv::compare(channel[0], color1, color1, CMP_GT);
	cv::compare(color, channel[0] + 50, color, CMP_LT);
	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_not(color, color1);

	setColor(channel, color, color1, 200, 90, 90);
}

void findYellow(Mat channel[]) {
	Mat color;
	Mat color1;
	Mat color2;
	cv::absdiff(channel[1], channel[2], color);
	cv::compare(color, Mat(channel[0].rows, channel[0].cols, CV_8UC1, 20), color, CMP_LT);
	color1 = cv::Mat(channel[2].rows, channel[2].cols, CV_8UC1, 140);
	cv::compare(channel[2], color1, color1, CMP_GT);
	cv::compare(channel[0], channel[2]/2, color2, CMP_LT);

	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_and(color, color2, color);
	cv::bitwise_not(color, color1);

	setColor(channel, color, color1, 30, 240, 240);
}

void findClearBlue(Mat channel[]) {
	Mat color;
	Mat color1;
	Mat color2;
	cv::absdiff(channel[1], channel[0], color);
	cv::compare(color, Mat(channel[0].rows, channel[0].cols, CV_8UC1, 20), color, CMP_LT);
	color1 = cv::Mat(channel[2].rows, channel[2].cols, CV_8UC1, 140);
	cv::compare(channel[1], color1, color1, CMP_GT);
	cv::compare(channel[2], channel[1]/2, color2, CMP_LT);

	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_and(color, color2, color);
	//(img[1].at<uchar>(Point(j, i)) - img[0].at<uchar>(Point(j, i)) > -20 &&
	//img[1].at<uchar>(Point(j, i)) - img[0].at<uchar>(Point(j, i)) < 20) &&
	//img[1].at<uchar>(Point(j, i)) > 140 &&
	//img[2].at<uchar>(Point(j, i)) < img[1].at<uchar>(Point(j, i))/2;
	cv::bitwise_not(color, color1);

	setColor(channel, color, color1, 240, 240, 30);
}

void findPurple(Mat channel[]) {
	Mat color;
	Mat color1;
	Mat color2;
	cv::absdiff(channel[0], channel[2], color);
	cv::compare(color, Mat(channel[0].rows, channel[0].cols, CV_8UC1, 20), color, CMP_LT);
	color1 = cv::Mat(channel[2].rows, channel[2].cols, CV_8UC1, 140);
	cv::compare(channel[0], color1, color1, CMP_GT);
	cv::compare(channel[1], channel[0]/2, color2, CMP_LT);

	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_and(color, color2, color);
	//img[0].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) > -20 &&
	//img[0].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) < 20) &&
	//img[0].at<uchar>(Point(j, i)) > 140 &&
	//img[1].at<uchar>(Point(j, i)) < img[0].at<uchar>(Point(j, i))/2;
	cv::bitwise_not(color, color1);

	setColor(channel, color, color1, 240, 30, 240);
}

void findWingsColor(Mat channel[]) {
        Mat rG;
        Mat bG;
        Mat gG;
	Mat rL;
        Mat bL;
        Mat gL;
       	Mat color;
	Mat color1;
	namedWindow("test1", 1);	
	cv::compare( Mat(channel[0].rows, channel[0].cols, CV_8UC1, 50), channel[2], gG, CMP_LT);
	cv::compare(channel[1], channel[0], rL, CMP_GT);	
	
	cv::add(channel[1], channel[0], bL);
	cv::add(channel[2], Mat(channel[0].rows, channel[0].cols, CV_8UC1, 10), bG);

	cv::compare(Mat(channel[0].rows, channel[0].cols, CV_8UC1, 15), abs(bG - bL), color, CMP_GT);
	cv::bitwise_and(color, gG, color);
	cv::bitwise_and(color, rL, color);
	
        // Getting binary image for color and its negative.
	cv::bitwise_not(color, color1);
        //img[0].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) > -20 &&
        //img[0].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) < 20) &&
        //img[0].at<uchar>(Point(j, i)) > 140 &&
        //img[1].at<uchar>(Point(j, i)) < img[0].at<uchar>(Point(j, i))/2;
        setColor(channel, color, color1, 255, 255, 255);
}


void setColor(Mat channel[], Mat color, Mat negativeColor, int B, int G, int R) {
	channel[0].setTo(B, color);
	channel[0].setTo(0, negativeColor);
	channel[1].setTo(G ,color);
	channel[1].setTo(0 , negativeColor);
	channel[2].setTo(R ,color);
	channel[2].setTo(0 , negativeColor);
}
