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

class VideoWasps {
	public:
		double _camDist;
		double _camDistFactor;
		double _duration;
		double _percentVideoPerFrame;
		int _fps;
		VideoWasps() {
			_camDistFactor = 2.0;
		}
};

//Number of wasp in screen
int waspNumber = 0;
int newWaspNumber;
float biggestContour = 0;
int frameNum = 0;
Mat prevImg = Mat();
Mat restaImg = Mat();
Mat cadaDiez[20];
VideoWasps vid = VideoWasps();

cv::VideoCapture cap;
int tbPos;
const int alpha_slider_max = 100;
int alpha_slider = 1;
double alpha;
double beta;
cv::Mat initialImage, splitedImages, frame, blurred, drawing, ids;

void dummy(int, void *);
void readme();
void initialize();
int openVideo(int argc, string videoPath);
void detectIds();
void moveDetection();
void postProcesado();

bool isWhite(Mat img[], int i, int j);
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
float distanceBetweenPoints(Point p1, Point p2);

void findAndSetColor(Mat image, char col, Mat &retImage);
void findWhite(Mat channel[]);
void findGreen(Mat channel[]);
void findRed(Mat channel[]);
void findBlue(Mat channel[]);
void findYellow(Mat channel[]);
void findClearBlue(Mat channel[]);
void findPurple(Mat channel[]);
void findWingsColor(Mat channel[]);
void setColor(Mat channel[], Mat color, Mat negativeColor, int B, int G, int R);
double diametroMayorEtiqueta(Mat img);
void mergeNearbyIds(vector<vector<Point> > &contours, vector<Point2f> &mc);
cv::Mat maskedImage(Mat id, Mat originalImage);
Mat maskedImageProcessing(Mat img);
vector<vector<Point> > getContoursWithCanny(Mat img, int cannyThres, int maxCannyThresh, int contType, int contWay);
vector<Point2f> getContoursMassCenters(vector<vector<Point> > contours);

//Deteccion del cuerpo
float getBodyOrientation(Mat img, Mat imgResta);
Rect dameRectanguloRecorte(int x, int y, Mat img, float contArea);
Point puntoFinalLinea(int x, int y, Mat img, float wihe, float rad);
float fitEllipseContour(Mat img, Mat prev);

class Wasp {
public:
	int _x;
	int _y;
	char _idColor;
	int _direction;
	int _wings;
	int _behaviour;
	Point _body;
	float _orientation;
	cv::Mat _heatMapPos;
	
	Wasp(int x, int y, cv::Mat img) {
		_x = x;
		_y = y;
		_heatMapPos = cv::Mat(img.rows, img.cols, CV_64FC1, 0.0);
	}
	Wasp() {}
	
	void setIdColor(Mat img) {
		Mat imgChannels[3];
		split(img, imgChannels);
	
		if (isYellow(imgChannels, _y, _x)) {
			_idColor = 'y';
		}
		else if (isClearBlue(imgChannels, _y, _x)) {
			_idColor = 'c';
		}
		else if (isPurple(imgChannels, _y, _x)) {
			_idColor = 'p';
		}
		/*else if (isWhite(imgChannels, _y, _x)) {
			_idColor = 'w';
		}*/
		else if (isGreen(imgChannels, _y, _x)) {
			_idColor = 'g';
		}
		else if (isBlue(imgChannels, _y, _x)) {
			_idColor = 'b';
		}
		else if (isRed(imgChannels, _y, _x)) {
			_idColor = 'r';
		}
	}
	
	void setNewPositionFromLastOne(Mat img) {
		const int maxSize = 4;
		int x1, x2, y1, y2;
		Mat section;
		vector<vector<Point> > contours;
		vector<Point2f> mc;
		
		float lastCamFactor = vid._camDistFactor;
		vid._camDistFactor = 4.0;
		if (vid._camDist <= 0)
			vid._camDist = 25;
		x1 = _x - (vid._camDist * vid._camDistFactor);
		x2 = _x + (vid._camDist * vid._camDistFactor);
		y1 = _y - (vid._camDist * vid._camDistFactor);
		y2 = _y + (vid._camDist * vid._camDistFactor);

		if (x1 < 0) {
			x1 = 0;
		}
		if (y1 < 0) {
			y1 = 0;
		}
		if (x2 >= (int)(img.size().width)) {
			x2 = img.size().width - 1;
		}
		if (y2 >= (int)(img.size().height)) {
			y2 = img.size().height - 1;
		}
		// Getting image with the colours of interest.
		section = maskedImage(section, img(Rect(Point(x1, y1), Point(x2, y2))));
		// Processing image 
		section = maskedImageProcessing(section);
		
		// Getting contourse from processed masked image
		contours = getContoursWithCanny(section, 50, 100, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
		// Getting mass centers for each contour
		mc = getContoursMassCenters(contours);
		
		vid._camDistFactor = lastCamFactor;
		int dist = 0;
		int sWasp = -1;
		Wasp wasps[maxSize];
		int wasp = 0;
		int center = (int)(vid._camDist * vid._camDistFactor);
		
		if (contours.size() > 0) {
			for( int i = 0, tmp; i < contours.size(); i++ )
			{
				if (mc[i].x > 0 && mc[i].y > 0 && i < maxSize) {
					wasps[wasp] = Wasp(mc[i].x, mc[i].y, section);
					wasps[wasp].setIdColor(section);
					if (wasps[wasp]._idColor == _idColor) {
						tmp = (int)(std::sqrt((mc[i].x - center)*(mc[i].x - center) + 
						(mc[i].y - center)*(mc[i].y - center)));
						if (tmp > dist) {
							dist = tmp;
							sWasp = wasp;
						}
						wasp++;
					}
				}
			}
			if (sWasp > -1) {
				_x = wasps[sWasp]._x + x1;
				_y = wasps[sWasp]._y + y1;
				cout << endl << _x << " " << _y << endl;
				this->incrementHeatMap(Point(_x, _y));
			}
		}
	}
	
	Scalar getIdColor() {
		Scalar color;
		
		if (_idColor == 'w') {
			color = cv::Scalar(255, 255, 255);
		}
		else if (_idColor == 'y') {
			color = cv::Scalar(30, 240, 240);
		}
		else if (_idColor == 'c') {
			color = cv::Scalar(240, 240, 30);
		}
		else if (_idColor == 'p') {
			color = cv::Scalar(240, 30, 240);
		}
		else if (_idColor == 'g') {
			color = cv::Scalar(90, 200, 90);
		}
		else if (_idColor == 'b') {
			color = cv::Scalar(200, 90, 90);
		}
		else if (_idColor == 'r') {
			color = cv::Scalar(90, 90, 200);
		}
		else {
			color = cv::Scalar(0, 0, 0);
		}
		
		return color;
	}
	
	void incrementHeatMap(Point pos) {
		_heatMapPos.at<double>(Point(pos.x, pos.y)) = _heatMapPos.at<double>(Point(pos.x, pos.y)) + vid._percentVideoPerFrame;
	}
};

class Node {
	public:
		Wasp _wasp;
		Node* _previous;
		Node* _next;
		Node(Wasp wasp) {
			_wasp = wasp;
		}
};

class WaspList{
	public:
		int _size;
		int _pos;
		Node* _first;
		WaspList() {
			_first = NULL;
			_size = 0;
		}
		int getSize() {
			return _size;
		}
		void addWasp(Wasp* wasp) {
			Node* node = new Node(*wasp);
			if (_size == 0) {
				_first = node;
				_first->_next = NULL;
				_first->_previous = NULL;
				_size = _size + 1;
			}
			else {
				Node* tmp = _first;
				_first = node;
				_first->_previous = tmp;
				_first->_next = NULL;
				tmp->_next = _first;
				_size = _size + 1;
			}
			
		}
		void removeWaspFromPos(int i) {
			if (_size == 1) {
				_first = NULL;
				_size = 0;
			}
			else if (_size >= 2) {
				if (_pos == _size - 1) {
					Node* tmp = _first;
					_first = _first->_previous;
					_first->_next = NULL;
					tmp = NULL;
				}
				else {
					Node* tmp = _first;
					for (int i = _size - 1; i > _pos; i--) {
						tmp = tmp->_previous;
					}
					if (_pos == 0) {
						tmp->_next->_previous = tmp->_previous;
						tmp = NULL;
					}
					else {
						tmp->_previous->_next = tmp->_next;
						tmp->_next->_previous = tmp->_previous;
						tmp = NULL;
					}
				}
			}
		}
		Wasp* getWaspFromPos(int pos){
			Node* tmp = _first;
			for (int i = _size - 1; i > pos; i--) {
				tmp = tmp->_previous;
			}
			return &tmp->_wasp;
		}	
};

Wasp* coincidentWasp(Wasp * test);
int waspsSimillarity(Wasp *wasp1, Wasp* wasp2);
void performGlobalMatching();
void performLocalMatching();
void previousIdsDetection();
void checkWaspsOrientation(Mat img);

// Global dynamic array which keeps the info about the Wasps to be followed.
Wasp** wasps = new Wasp*[10];
Wasp** waspsTest = new Wasp*[10];
WaspList waspsList = WaspList();
WaspList waspsListTest = WaspList();

int main( int argc, char** argv )
{
	for(int f = 0; f < 19; f++)
		cadaDiez[f] = Mat();
	waspsListTest = WaspList();
	waspsList = WaspList();
	detectIds();
}

void initialize() {
	alpha_slider = 1;
	frame = Mat();
	blurred = Mat();
	cap.open("multimedia/video/17/00056.MTS");
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

	initialize();
	
	//Video properties
	vid._fps = cap.get(CV_CAP_PROP_FPS);
	vid._duration = cap.get(CV_CAP_PROP_FRAME_COUNT);
	vid._percentVideoPerFrame = 1.0 / vid._duration;
	
	//Windows to be shown
	namedWindow("video", 1);
	namedWindow("test", 1);
	
	for(;;)
	{
		cap >> frame;
		if (frame.data) {
			frameNum++;
			initialImage = frame.clone();
			resize(frame, initialImage, Size(700, 550), 0, 0, INTER_CUBIC);
			if(!initialImage.data)
			{
				printf("Error: no frame data.\n");
				break;
			}
			if (frameNum % 50 == 1)
				performGlobalMatching();
			else {
				performLocalMatching();
			}
			cout << "frame " << frameNum << endl;
			imshow("video", drawing);
			imshow("test", ids);
			cv::waitKey(30);
		}
	}
	//cv::waitKey(0);
}

bool isWhite(Mat img[], int i, int j) {
	return img[0].at<uchar>(Point(j, i)) > 239 && img[1].at<uchar>(Point(j, i)) > 239 &&
		img[2].at<uchar>(Point(j, i)) > 239;
}

bool isGreen(Mat img[], int i, int j) {
	return img[0].at<uchar>(Point(j, i)) + img[2].at<uchar>(Point(j, i)) < 
		img[1].at<uchar>(Point(j, i))+10 && img[1].at<uchar>(Point(j, i)) > 40;
}

bool isRed(Mat img[], int i, int j) {
	return img[0].at<uchar>(Point(j, i))+ img[1].at<uchar>(Point(j, i)) < 
		img[2].at<uchar>(Point(j, i))+10  && img[2].at<uchar>(Point(j, i)) > 40;
}

bool isBlue(Mat img[], int i, int j) {
	return img[1].at<uchar>(Point(j, i)) + img[2].at<uchar>(Point(j, i)) < 
		img[0].at<uchar>(Point(j, i))+10 && img[0].at<uchar>(Point(j, i)) > 40;
}

bool isYellow(Mat img[], int i, int j) {
	return (img[1].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) > -20 &&
		img[1].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) < 20) &&
		img[2].at<uchar>(Point(j, i)) > 40 &&
		img[0].at<uchar>(Point(j, i)) < img[2].at<uchar>(Point(j, i))/2;
}

bool isClearBlue(Mat img[], int i, int j) {
	return (img[1].at<uchar>(Point(j, i)) - img[0].at<uchar>(Point(j, i)) > -20 &&
		img[1].at<uchar>(Point(j, i)) - img[0].at<uchar>(Point(j, i)) < 20) &&
		img[1].at<uchar>(Point(j, i)) > 40 &&
		img[2].at<uchar>(Point(j, i)) < img[1].at<uchar>(Point(j, i))/2;
}

bool isPurple(Mat img[], int i, int j) {
	return (img[0].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) > -20 &&
		img[0].at<uchar>(Point(j, i)) - img[2].at<uchar>(Point(j, i)) < 20) &&
		img[0].at<uchar>(Point(j, i)) > 40 &&
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
	retImage = Mat::zeros(image.rows, image.cols, CV_BGR2GRAY);
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

void findWhite(Mat channel[]) {
	Mat color;
	Mat color1;
	Mat color2;
	cv::compare(cv::Mat(channel[0].rows, channel[0].cols, CV_8UC1, 255) - channel[0], cv::Mat(channel[0].rows, channel[0].cols, CV_8UC1, 15), color, CMP_LT);
	cv::compare(cv::Mat(channel[1].rows, channel[1].cols, CV_8UC1, 255) - channel[1], cv::Mat(channel[1].rows, channel[1].cols, CV_8UC1, 15), color1, CMP_LT);
	cv::compare(cv::Mat(channel[0].rows, channel[0].cols, CV_8UC1, 255) - channel[2], cv::Mat(channel[0].rows, channel[0].cols, CV_8UC1, 15), color2, CMP_LT);
	
	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_and(color, color2, color);
	cv::bitwise_not(color, color1);
	
	setColor(channel, color, color1, 255, 255, 255);
}

void findGreen(Mat channel[]) {
	Mat color;
	Mat color1;
	Mat color2;
	color = channel[0] + channel[2];
	color1 = cv::Mat(channel[0].rows, channel[0].cols, CV_8UC1, 140);
	cv::compare(channel[1], color1, color1, CMP_GT);
	cv::compare(channel[0], channel[1] - 25, color, CMP_LT);
	cv::compare(channel[2], channel[1] - 25, color2, CMP_LT);
	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_and(color, color2, color);
	cv::bitwise_not(color, color1);

	setColor(channel, color, color1, 90, 200, 90);
}

void findRed(Mat channel[]) {
	Mat color;
	Mat color1;
	Mat color2;
	Mat color3;
	color = channel[0] + channel[1];
	color1 = cv::Mat(channel[2].rows, channel[2].cols, CV_8UC1, 140);
	cv::compare(channel[2], color1, color1, CMP_GT);
	cv::compare(channel[0], channel[2] - 50, color, CMP_LT);
	cv::compare(channel[1], channel[2] - 50, color2, CMP_LT);
	cv::compare(abs(channel[0] - channel[1]), cv::Mat(channel[2].rows, channel[2].cols, CV_8UC1, 30), color3, CMP_LT);
	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_and(color, color2, color);
	cv::bitwise_and(color, color3, color);
	cv::bitwise_not(color, color1);

	setColor(channel, color, color1, 90, 90, 200);
}

void findBlue(Mat channel[]) {
	Mat color;
	Mat color1;
	Mat color2;
	Mat color3;
	color = channel[1] + channel[2];
	color1 = cv::Mat(channel[0].rows, channel[2].cols, CV_8UC1, 140);
	cv::compare(channel[0], color1, color1, CMP_GT);
	cv::compare(channel[1], channel[0] - 40, color, CMP_LT);
	cv::compare(channel[2], channel[0] - 40, color2, CMP_LT);
	//cv::compare(abs(channel[1] - channel[2]), cv::Mat(channel[2].rows, channel[2].cols, CV_8UC1, 30), color3, CMP_LT);
	
	
	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_and(color, color2, color);
	//cv::bitwise_and(color, color3, color);
	cv::bitwise_not(color, color1);

	setColor(channel, color, color1, 200, 90, 90);
}

void findYellow(Mat channel[]) {
	Mat color;
	Mat color1;
	Mat color2;
	Mat color3;
	cv::absdiff(channel[1], channel[2], color);
	cv::compare(color, Mat(channel[0].rows, channel[0].cols, CV_8UC1, 20), color, CMP_LT);
	cv::compare(channel[2], cv::Mat(channel[2].rows, channel[2].cols, CV_8UC1, 140), color1, CMP_GT);
	cv::compare(channel[1], cv::Mat(channel[2].rows, channel[2].cols, CV_8UC1, 140), color3, CMP_GT);
	cv::compare(channel[0], 2*channel[2]/3, color2, CMP_LT);

	// Getting binary image for color and its negative.
	cv::bitwise_and(color, color1, color);
	cv::bitwise_and(color, color2, color);
	cv::bitwise_and(color, color3, color);
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

void setColor(Mat channel[], Mat color, Mat negativeColor, int B, int G, int R) {
	channel[0].setTo(0, negativeColor);
	channel[0].setTo(B, color);
	channel[1].setTo(0 , negativeColor);
	channel[1].setTo(G ,color);
	channel[2].setTo(0 , negativeColor);
	channel[2].setTo(R ,color);
}

double diametroMayorEtiqueta(Mat img) {

	//Variables auxiliares
	Mat auxMat;
	vector<vector<Point> > contours;
	int thresh = 50;
	vector<Vec4i> hierarchy;
	
	//Antes de aplicar canny, pasamos a binario la imagen
	cvtColor(img, auxMat, CV_BGR2GRAY);

	//pasamos todo lo que no es negro a blanco y el resto a negro   
	threshold( auxMat, auxMat, 30, 255 ,THRESH_BINARY );

	// Detect edges using canny
	Canny( auxMat, auxMat, thresh, thresh*2, 3 );

	//miramos la imagen resultante
	//namedWindow("DentroDeLaFuncion",CV_WINDOW_NORMAL);
	//cv:imshow("DentroDeLaFuncion", auxMat);

	// Find contours
	findContours( auxMat, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

	// Sacamos el area de los contornos y nos quedamos con el mejor
	double best = 0;
	for(int i = 1; i < contours.size(); i++)
	{
		double asd = contourArea(contours[i]);
		if(asd > best)
			best = asd;
			
		
	}

	//Sacamos el diametro del mejor contorno
	double diameter = sqrt(best / 3.1416) * 2;

	return diameter;
}

void mergeNearbyIds(vector<vector<Point> > &contours, vector<Point2f> &mc) {
	for( int i = 0; i < contours.size(); i++ ) {
		for (int j = 0; j < contours.size(); j++) {
			if (i != j && std::sqrt((mc[i].x - mc[j].x)*(mc[i].x - mc[j].x) + 
				(mc[i].y - mc[j].y)*(mc[i].y - mc[j].y)) < vid._camDistFactor * vid._camDist) {
					mc[j].operator =(Point(-100, -100));
			}
		}
	}
}

Wasp* coincidentWasp(Wasp* test) {
	int numWasp = 0;
	int bestWasp = 0;
	int points = 0;
	int tempPoints = 0;
	cout << "size " << sizeof(*wasps) << endl;
	while (numWasp < sizeof(*wasps) / sizeof(wasps[0])) {
		cout << numWasp << endl;
		tempPoints = waspsSimillarity(wasps[numWasp], test);
		if (tempPoints > points) {
			points = tempPoints;
			bestWasp = numWasp;
		}
		
		numWasp++;
	}
	
	if (points > 80) {
		test = wasps[bestWasp];
	}
	else {
		test->_x = -1;
		test->_y = -1;
		test->_direction = -1;
		test->_wings = -1;
		test->_behaviour = -1;
	}
	
	return test;
}

int waspsSimillarity(Wasp *wasp1, Wasp* wasp2) {
	double distance;

	//compare position
	distance = std::sqrt(double((wasp1->_x - wasp2->_x)*(wasp1->_x - wasp2->_x)+(wasp1->_y-wasp2->_y)*(wasp1->_y-wasp2->_y)));
	cout << "dist: " << distance << endl;
	//compare direction
	//compare wings
	//compare color
	//compare behaviour
	
	return (int)distance;
};


void performGlobalMatching() {
	/*First of all we look for possible matches based on the colour of the wasp's ids.
	The waspsTest list of wasps is refreshed with the new info.*/
	previousIdsDetection();

	/* Now we check the potential results by finding orientation of the suggested wasps.
	If no result is given for a certain wasp, it is deleted from the list.*/
	
	//COMcheckWaspsOrientation();
	
	//Post Procesado
	//COMpostProcesado();
	
	//Seria aqui la llamada a la funcion de deteccion de los cuerpos?
	
	
	//Mat hsv;
	//cvtColor(initialImage,hsv, COLOR_BGR2HSV);
	//Canny(hsv, hsv, 150, 200,3);
	//namedWindow("hsv",1);
	//imshow("hsv",hsv);
}

void performLocalMatching() {
	drawing = initialImage.clone();
	int listSize = waspsList.getSize();

	for (int i = 0; i < (int)listSize; i++) {
		waspsList.getWaspFromPos(i)->setNewPositionFromLastOne(initialImage);
		circle( drawing, Point(waspsList.getWaspFromPos(i)->_x, waspsList.getWaspFromPos(i)->_y), 4, waspsList.getWaspFromPos(i)->getIdColor(), -1, 8, 0 );
	}
}


void postProcesado() {	

	/*
		Doble bucle para sacar que avispas estan muy cerca
	*/
	for(int i1 = 0; i1 < waspsListTest.getSize(); i1++) {
		for(int i2 = i1 + 1; i2 < waspsListTest.getSize(); i2++) {
		
			Point e1(waspsListTest.getWaspFromPos(i1)->_x,waspsListTest.getWaspFromPos(i1)->_y);
			Point c1 = waspsListTest.getWaspFromPos(i1)->_body;
			
			Point e2(waspsListTest.getWaspFromPos(i2)->_x,waspsListTest.getWaspFromPos(i2)->_y);
			Point c2 = waspsListTest.getWaspFromPos(i2)->_body;
			
			//Como algoritmo inicial vamos a ver las distancias entre los puntos 2 a 2, mas adelante habrá que tener encuenta la orientacion
			if(distanceBetweenPoints(c1,c2) < 150 || distanceBetweenPoints(c1,e2) < 150 || distanceBetweenPoints(e1,c2) < 150 || distanceBetweenPoints(e1,e2) < 150)
				cout << "avispas(" <<  i1 << " - " << i2 << ")" << endl;
		
		}
	}
}

float distanceBetweenPoints(Point p1, Point p2) {
	return sqrt(pow((double)(p2.x - p1.x), 2) + pow((double)(p2.y - p1.y), 2) );
}

cv::Mat maskedImage(Mat img, Mat originalImage) {
	Mat splitedImages;

	//findAndSetColor(initialImage, 'w', splitedImages);
	//ids = splitedImages;
	findAndSetColor(originalImage, 'g', splitedImages);
	img = splitedImages;
	findAndSetColor(originalImage, 'b', splitedImages);
	img = img + splitedImages;
	findAndSetColor(originalImage, 'r', splitedImages);
	img = img + splitedImages;
	findAndSetColor(originalImage, 'y', splitedImages);
	img = img + splitedImages;
	findAndSetColor(originalImage, 'p', splitedImages);
	img = img + splitedImages;
	findAndSetColor(originalImage, 'c', splitedImages);
	img = img + splitedImages;
	
	return img;
}

Mat maskedImageProcessing(Mat img) {
	int erosionSize = 1;
	int erosionType = 2;
	Mat element1 = getStructuringElement( erosionType,
		Size( 2*erosionSize + 1, 2*erosionSize+1 ),
		Point( erosionSize, erosionSize ) );
		
	Mat element2 = getStructuringElement( erosionType,
		Size( 10*erosionSize + 1, 10*erosionSize+1 ),
		Point( 5*erosionSize, 5*erosionSize ) );

	/// Apply the filtering
	blur( img, img, Size( erosionSize*5, erosionSize*5 ), Point(-1,-1) );
	erode( img, img, element1);
	dilate( img, img, element2);
	
	/* We blur the result image so that the nearby results (usually belonging to the same wasp)
	get merged.*/
	blur( img, img, Size( erosionSize*5, erosionSize*5 ), Point(-1,-1) );
	
	return img;
}


vector<vector<Point> > getContoursWithCanny(Mat img, int cannyThres, int maxCannyThresh, int contType, int contWay) {
	Mat canny;
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	
	// Detect edges using canny
	Canny( img, canny, cannyThres, maxCannyThresh, 3 );
	/// Find contours
	findContours( canny, contours, hierarchy, contType, contWay, Point(0, 0) );
	
	return contours;
}

vector<Point2f> getContoursMassCenters(vector<vector<Point> > contours) {
	/// Get the moments
	vector<Moments> mu(contours.size() );
	for( int i = 0; i < contours.size(); i++ )
	{ mu[i] = moments( contours[i], false ); }

	///  Get the mass centers:
	vector<Point2f> mc( contours.size() );
	for( int i = 0; i < contours.size(); i++ )
	{ mc[i] = Point2f( mu[i].m10/mu[i].m00 , mu[i].m01/mu[i].m00 ); }
	
	return mc;
}


void previousIdsDetection() {
	int thresh = 50;
	int max_thresh = 100;
	RNG rng(12345);
	cv::Mat image, channel[3], canny;
	vector<vector<Point> > contours;
	vector<Point2f> mc( NULL );

	// Getting image with the colours of interest.
	ids = maskedImage(ids, initialImage);
	// Processing image 
	ids = maskedImageProcessing(ids);
	// Getting contourse from processed masked image
	contours = getContoursWithCanny(ids, 50, 100, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
	// Getting mass centers for each contour
	mc = getContoursMassCenters(contours);
	// Here we calculate the camera distance
	vid._camDist = diametroMayorEtiqueta(ids);
	// We merge the detected nearby wasps to just one
	mergeNearbyIds(contours, mc);

	/// Draw contours
	Wasp* test;
	int wasp = 0;
	drawing = initialImage.clone();
	//split(ids, channel);
 	waspsListTest = WaspList();
	if (waspsListTest.getSize() >= 0) {
		for( int i = 0; i < contours.size(); i++ )
		{
			if (mc[i].x > 0 && mc[i].y > 0) {
				waspsListTest.addWasp(new Wasp(mc[i].x, mc[i].y, ids));
				//waspsTest[wasp] = new Wasp(mc[i].x, mc[i].y, ids);
				waspsListTest.getWaspFromPos(wasp)->setIdColor(ids);
				//waspsTest[wasp]->setIdColor(ids);
				
				//drawContours( drawing, contours, i, color, 2, 8, hierarchy, 0, Point() );
				//circle( drawing, Point(waspsTest[wasp]->_x, waspsTest[wasp]->_y), 4, waspsTest[wasp]->getIdColor(), -1, 8, 0 );
				circle( drawing, Point(waspsListTest.getWaspFromPos(wasp)->_x, waspsListTest.getWaspFromPos(wasp)->_y), 4, waspsListTest.getWaspFromPos(wasp)->getIdColor(), -1, 8, 0 );
				
				//waspsListTest.getWaspFromPos(wasp)->incrementHeatMap(Point(waspsListTest.getWaspFromPos(wasp)->_x,waspsListTest.getWaspFromPos(wasp)->_y));
				wasp++;
			}
		}
	}
	
	// TODO
	waspsList = waspsListTest;
	
	newWaspNumber = wasp;
}


void checkWaspsOrientation(Mat img) {
	/*
	1. Miramos si el numero de avispas en la imagen ha cambiado
		1.1 si es asi guardamos el contorno mas grande como contorno de referencia
	2. Recorremos las avispas para sacar el cuerpo
		2.1 Sacamos el centro de la etiqueta, y recortamos en funcion del contorno mas grande
		2.2 Sacamos el grado de inclinacion de la linea y lo guardamos en la avispa
	3. Pintamos la linea del cuerpo en la imagen que se va a mostrar luego
	
	*/
	
	if(prevImg.empty()) {
		prevImg = img.clone();
		for(int f = 0; f < 20; f++) {
			cadaDiez[f] = img.clone();	
			cout << "ha: " << cadaDiez[f].size().width << endl;
		cout << "haaaaa: " << cadaDiez[f].size().height << endl;
			}
	}
	else {
	for(int f = 0; f < 19; f++)
		cadaDiez[f] = cadaDiez[f + 1].clone();
		
	cadaDiez[19] = img.clone();
	}
	Mat laDiez = Mat();
	
	laDiez = abs(cadaDiez[19] - cadaDiez[0]);
	
	Canny(laDiez, laDiez, 150, 200,3);
	//AQUI-si
	
	int erosionSize = 2;
	int erosionType = 2;
	Mat element = getStructuringElement( erosionType,
		Size( 2*erosionSize + 1, 2*erosionSize+1 ),
		Point( erosionSize, erosionSize ) );

	/// Apply the operation
	blur( laDiez, laDiez, Size( erosionSize*5, erosionSize*5 ), Point(-1,-1) );
	erode( laDiez, laDiez, element );
	dilate( laDiez, laDiez, element );
	threshold(laDiez, laDiez,1,255,0);
	
	blur( laDiez, laDiez, Size( 20, 20 ), Point(-1,-1) );
	
	threshold(laDiez, laDiez,1,255,0);
	
	erode( laDiez, laDiez, element );
	
	//hacemos los recortes y
	/*Esto es lo que tiene que estar dentrode la funcion de busqueda de avispas
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	findContours( laDiez, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

	for( int i = 1; i < contours.size(); i++)
	{
		
		RotatedRect el = fitEllipse(contours[i]);
		cout << "**Contorno " << i << ":" << endl;
		cout << "   Ancho: " << el.size.width << endl;
		cout << "   Alto: " << el.size.height << endl;
		
		double asd = contourArea(contours[i]);

		cout << "contorno: " << asd << endl;
		
	}
	
	namedWindow("restaFrames", 1);
	imshow("restaFrames", laDiez);
	*/
	
	
	absdiff(img, prevImg, restaImg);
	
	//Si no hay avispas no hacemos nada
	if(newWaspNumber == 0)
		return;
		
	// 1. Miramos si el numero de avispas en la imagen ha cambiado
	if(waspNumber != newWaspNumber) {
		if(vid._camDist > biggestContour)
			biggestContour = vid._camDist;
	}
	
	//Imagen que mostraremos con los cuerpos
	Mat imagenResultado = img.clone();
	//2. Recorremos las avispas para sacar el cuerpo
	
	for(int i = 0; i < waspsListTest.getSize(); i++) {
	
		Rect rectangulo = dameRectanguloRecorte(waspsListTest.getWaspFromPos(i)->_x, waspsListTest.getWaspFromPos(i)->_y, imagenResultado, biggestContour);
	
		Mat recorte = img(rectangulo);
		Mat recorteResta = laDiez(rectangulo);
		//img(rectangulo).copyTo(recorte);
		
		//float angEllipse = fitEllipseContour(recorteResta);
		
		
		//sacamos los radianes de inclinacion
		float rads = getBodyOrientation(recorte, recorteResta);
		
		//pintamos la linea
		//sacamos el punto final de la linea
		float longitud = biggestContour * 3.5;
		
		Point p = puntoFinalLinea(waspsListTest.getWaspFromPos(i)->_x, waspsListTest.getWaspFromPos(i)->_y, imagenResultado, longitud, rads);
		Point etiqueta(waspsListTest.getWaspFromPos(i)->_x, waspsListTest.getWaspFromPos(i)->_y);
		
		//Guardamos el punto final del cuerpo
		waspsListTest.getWaspFromPos(i)->_body = p;
		
		//3. Pintamos la linea del cuerpo en la imagen que se va a mostrar luego
		line(imagenResultado, p, etiqueta, Scalar(255,0,0), 10, 8, 0);
	}
	
	namedWindow("lineaPintada",1);
	imshow("lineaPintada",imagenResultado);
	
	
	//pasamos todo lo que no es negro a blanco y el resto a negro
	/*   
	threshold( restaImg, restaImg, 20, 255 ,THRESH_BINARY );
	namedWindow("zzz", 1);
	imshow("zzzz", restaImg);
	prevImg = img.clone();
	*/
	
	/* Esto era para las alas, no da buenos resultados con los videos de Isma
	Mat testAlas = img.clone();
	cv::Mat chaTest[3];
	split(testAlas, chaTest);
	findWingsColor(chaTest);
	merge(chaTest, 3, testAlas);
	Mat element = getStructuringElement( 1,
                    Size( 2*0.5 + 1, 2*0.5+1 ),
                    Point( 1, 1 ) );

            /// Apply the erosion operation
            erode( testAlas, testAlas, element );

	//erode(test, test, Mat(), Point(-1, -1), 2, 1, 1);
	namedWindow("alas",1);
	imshow("alas", testAlas);
	
	
	Mat alas = imread("naranja.jpg");
	Mat re;
	matchTemplate( img, alas, re, 3);
	threshold( re, re, 0.9, 1 ,THRESH_BINARY );
	namedWindow("matchtemplate 3",1);
	imshow("matchtemplate 3",re);
	*/
	
}

float getBodyOrientation(Mat img, Mat imgResta) {
	
	float score = 2550;
	Point best;
	float bestAngle;
	float bestRadian = -1;
	float distSmall = 20;
	Mat bimg, gimg, rimg;
	
	Mat z = img.clone();
	Point central(img.size().width / 2, img.size().height / 2);
	
	//Primero sacamos contornos y vemos si hay alguno que contenga a la etiqueta y que no sea muy circular
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	findContours( imgResta, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
	bool contornoValido = false;
	for( int i = 1; i < contours.size(); i++)
	{
		
		RotatedRect el = fitEllipse(contours[i]);
		//Sacamos su left y top para el punto superior izquireda y con width y height sacamos el inferior derecha y miramos si contiene al punto central
		Point2f vertices[4];
		el.points(vertices);
		for( int x = 0; x < 4; x++)
		{
			cout << "vertice " << x << " : " << vertices[x].x << " , " << vertices[x].y;
		}
		//el.size.width
		//el.size.height
		
		//ahora hay que mirar si cumple que la elipse es lo suficientemente achatada
		
		//si todo va bien, entonces sacamos el angulo de la elipse
		float angle = el.angle;
		
		double asd = contourArea(contours[i]);
	}
	
	//Bucle de grados en los que inclinar la linea
	for(float gr = 0; gr < 360; gr += 1) {
		float rad = gr * 0.0174532925;
		float dist = img.size().width / 20 * 8;
		//Circulo grande donde acabaran las lineas
		Point p(dist * cos(rad) + img.size().width / 2 , dist * sin(rad) + img.size().width / 2);
		//circulo pequeño para que la linea no coja la etiqueta
		Point ps(distSmall * cos(rad) + img.size().width / 2 , distSmall * sin(rad) + img.size().width / 2);
		//creamos una imagen entera negra
		Mat a = Mat::zeros(img.size(), 16);
		//a.setTo(Scalar(15,15,30));
		line(a, p, ps, Scalar(255,255,255), 10, 8, 0);
		
		//creamos la linea para la cabeza
		Point p2( central.x - (p.x - central.x) / 5, central.y - (p.y - central.y) / 5);
		Point ps2( central.x - (ps.x - central.x), central.y - (ps.y - central.y));
		line(a, p2, ps2, Scalar(255,255,255), 12, 8, 0);
		
		Mat aux = img & a;		
		
		//inRange
		Mat asd;
		inRange(aux, Scalar(0,0,0), Scalar(1,1,1),asd);
		//Todo lo negro puro lo pasamos a marron oscuro
		aux.setTo(Scalar(24,16,29),asd);
		
		//Sacamos la media y dista menos del marron que la actual nos quedamos con ella
		Scalar media = mean(aux);
		double ladist = abs(media[0] - 12) + abs(media[1] - 7) + abs(media[2] - 17);
		if( ladist < score) {
			bestRadian = rad;
			bestAngle = gr;
			best = p;
			score = ladist;
			bimg = aux;
		}
		
		//circle(img, p, 1, Scalar(0,255,0), 1, 8, 0);
		//circle(img, ps, 1, Scalar(0,0,255), 1, 8, 0);
		
		//namedWindow("asddd", 1);
		//imshow("asddddd", img);
		
		
	}
	
	return bestRadian;

}

Rect dameRectanguloRecorte(int x, int y, Mat img, float contArea) {
	//Sacamos el ancho y el alto en funcion del tamaño de la etiqueta
	float wihe = contArea * 3.5;
	int left = 0;
	int top = 0;
	
	//Si nos salimos de los bordes, adaptamos la anchura y altura para que la etiqueta siga centrada
	//vemos los 4 posibles casos y nos quedamos pues con el menor
	if( y - wihe < 0 )
		wihe = y;
	if( y + wihe > img.size().height )
		wihe = img.size().height - y;
	if( x - wihe < 0 )
		wihe = x;
	if( x + wihe > img.size().width )
		wihe = img.size().width - x;
		
	/*
	//Comprobamos si nos salimos en vertical
	if((y - wihe) < 0) {
		top = 0;
	}else if( y + wihe > img.size().height ) {
		top = img.size().height - wihe * 2;
	} else {
		top = y - wihe;
	}
	
	//Comprobamos si nos salimos en horizontal
	if((x - wihe) < 0) {
		left = 0;
	}else if( x + wihe > img.size().width ) {
		left = img.size().width - wihe * 2;
	} else {
		left = x - wihe;
	}
	*/
	
	top = y - wihe;
	left = x - wihe;
	Rect ret = Rect(left, top, wihe*2, wihe*2);
	
	return ret;
}

Point puntoFinalLinea(int x, int y, Mat img, float wihe, float rad) {

	float left = wihe * cos(rad) + x;
	if(left < 0 ) left = 0;
	if(left > img.size().width) left = img.size().width;
	
	float top = wihe * sin(rad) + y;
	if(top < 0) top = 0;
	if(top > img.size().height) top = img.size().height;
	
	Point ret(left,top);
	
	return ret;	
}

//Devuelve el angulo de la ellipse
float fitEllipseContour(Mat resta) {
/*
1. hacer la resta
2. Hacer un blur muy tocho
3. pasar el canny y la busqueda de contornos
4. Quedarnos con el contorno mas grande que encuentre
5. Hacerle fit elipse
6. sacar el angulo de la elipse
7. pasar ese angulo a otro funcion, que hace la busqueda de marrones con +-30 grados
	7.1 puede llamarse a esta funcion desde la de marrones, tonces la busqueda de marrones se hace despues de esto
8. Mostrar
*/


return 0.0;
/*
	Mat canny;
   /// Detect edges using canny
  Canny( ids, canny, thresh, thresh*2, 3 );
  /// Find contours
//cvtColor(canny, canny, CV_BGR2GRAY);
  findContours( canny, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

for( int i = 1; i < contours.size(); i++)
{
	RotatedRect el = fitEllipse(contours[i]);
	cout << "**Contorno " << i << ":" << endl;
	cout << "   Ancho: " << el.size.width << endl;
	cout << "   Alto: " << el.size.height << endl;
	ellipse
}
*/
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