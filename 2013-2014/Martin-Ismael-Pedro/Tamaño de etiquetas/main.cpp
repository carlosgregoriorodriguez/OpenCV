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
Point followInterestPoint(Mat image, Mat tpl, Point interestPoint, int squareSize);
Point detectInterestPointFromTemplate (Mat tpl);
void on_trackbar(int valor,void*);
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





int main( int argc, char** argv )
{
    detectIds();

    return 0;
	
}


void detectIds() {
	namedWindow("adios",CV_WINDOW_NORMAL);
	namedWindow("hola",CV_WINDOW_NORMAL);
	int erosionSize = 1;
	int erosionType = 2;
	int thresh = 50;
	int max_thresh = 100;
	RNG rng(12345);
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	cv::Mat initialImage = cv::imread("multimedia/images/wasps.jpg");
	cv::Mat channel[3];
	channel[0] = Mat::zeros(initialImage.rows, initialImage.cols, CV_BGR2GRAY);
	channel[1] = Mat::zeros(initialImage.rows, initialImage.cols, CV_BGR2GRAY);
	channel[2] = Mat::zeros(initialImage.rows, initialImage.cols, CV_BGR2GRAY);
	cv::Mat image;
	cv::Mat splitedImages[6];
	cv::Mat ids;
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

    // green ids
    split(initialImage, channel);
    for (int i= 0; i < initialImage.rows; i++) {
		for (int j= 0; j < initialImage.cols; j++) { 
		
			if (isGreen(channel, i, j)) {
				setGreen(channel, i, j);
			}
			else {
				setBlack(channel, i, j);
			}
		}
    }
    merge(channel,3,splitedImages[0]);
  
    // red ids
    split(initialImage, channel);
    for (int i= 0; i < initialImage.rows; i++) {
		for (int j= 0; j < initialImage.cols; j++) { 
			if (isRed(channel, i, j)) {
				setRed(channel, i, j);
			}
			else {
				setBlack(channel, i, j);
			}
		}
    }
    merge(channel,3,splitedImages[1]);
    
    // blue ids
    split(initialImage, channel);
    for (int i= 0; i < initialImage.rows; i++) {
		for (int j= 0; j < initialImage.cols; j++) { 
			if (isBlue(channel, i, j)) {
				setBlue(channel, i, j);
			}
			else {
				setBlack(channel, i, j);
			}
		}
    }
    merge(channel,3,splitedImages[2]);
    
    // yellow ids
    split(initialImage, channel);
    for (int i= 0; i < initialImage.rows; i++) {
		for (int j= 0; j < initialImage.cols; j++) { 
			if (isYellow(channel, i, j)) {
				setYellow(channel, i, j);
			}
			else {
				setBlack(channel, i, j);
			}
		}
    }
    merge(channel,3,splitedImages[3]);
    
    // clear blue ids
    split(initialImage, channel);
    for (int i= 0; i < initialImage.rows; i++) {
		for (int j= 0; j < initialImage.cols; j++) { 
			if (isClearBlue(channel, i, j)) {
				setClearBlue(channel, i, j);
			}
			else {
				setBlack(channel, i, j);
			}
		}
    }
    merge(channel,3,splitedImages[4]);
    
    // purple ids
    split(initialImage, channel);
    for (int i= 0; i < initialImage.rows; i++) {
		for (int j= 0; j < initialImage.cols; j++) { 
			if (isPurple(channel, i, j)) {
				setPurple(channel, i, j);
			}
			else {
				setBlack(channel, i, j);
			}
		}
    }
    merge(channel,3,splitedImages[5]);
    
    ids = splitedImages[0] + splitedImages[1] + splitedImages[2] + splitedImages[3] + 
		splitedImages[4] + splitedImages[5];
    
    Mat element = getStructuringElement( erosionType,
		Size( 2*erosionSize + 1, 2*erosionSize+1 ),
        Point( erosionSize, erosionSize ) );

	/// Apply the erosion operation
	blur( ids, ids, Size( erosionSize*5, erosionSize*5 ), Point(-1,-1) );
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
//cvtColor(canny, canny, CV_BGR2GRAY);
  findContours( canny, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

for( int i = 1; i < contours.size(); i++)
{
	RotatedRect el = fitEllipse(contours[i]);
	cout << "Contorno " << i << ":" << endl;
	cout << " Ancho: " << el.size.width << endl;
	cout << " Alto: " << el.size.height << endl << endl;
}
/* Recorrerlo sacando el area del contorno
	for( int i = 0; i < contours.size(); i++)
{
	double asd = contourArea(contours[i]);
	cout << asd << endl;
}
*/
    
    cv::imshow("hola", ids);
    cv::imshow("adios", initialImage);
    cv::waitKey(0);
	
	
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
