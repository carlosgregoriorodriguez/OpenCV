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

cv::VideoCapture cap;
int tbPos;
const int alpha_slider_max = 100;
int alpha_slider = 1;
double alpha;
double beta;
cv::Mat splitedImages, frame, blurred, previousFrame;

void dummy(int, void *);
void readme();
void initialize();
int openVideo(int argc, string videoPath);
void detectIds();
void moveDetection();

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

void findAndSetColor(Mat image, char col, Mat &retImage);
void findWhite(Mat channel[]);
void findGreen(Mat channel[]);
void findRed(Mat channel[]);
void findBlue(Mat channel[]);
void findYellow(Mat channel[]);
void findClearBlue(Mat channel[]);
void findPurple(Mat channel[]);
void setColor(Mat channel[], Mat color, Mat negativeColor, int B, int G, int R);
double diametroMayorEtiqueta(Mat img);
void mergeNearbyIds(vector<vector<Point> > &contours, vector<Point2f> &mc);
VideoWasps vid = VideoWasps();

//Deteccion del cuerpo
float getBodyOrientation(Mat img);
Rect dameRectanguloRecorte(int x, int y, Mat img, float contArea);
Point puntoFinalLinea(int x, int y, Mat img, float wihe, float rad);

class Wasp {
public:
	int _x;
	int _y;
	char _idColor;
	int _direction;
	int _wings;
	int _behaviour;
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
void performGlobalMatching(Mat initialImage);
void previousIdsDetection(Mat initialImage);
void checkWaspsOrientation(Mat img);

// Global dynamic array which keeps the info about the Wasps to be followed.
Wasp** wasps = new Wasp*[10];
Wasp** waspsTest = new Wasp*[10];
WaspList waspsList = WaspList();
WaspList waspsListTest = WaspList();

int main( int argc, char** argv )
{
	detectIds();
}

void initialize() {
	alpha_slider = 1;
	frame = Mat();
	blurred = Mat();
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
	cv::Mat initialImage;

	initialize();
	
	cap.open("multimedia/v1.MTS");
	vid._fps = cap.get(CV_CAP_PROP_FPS);
	vid._duration = cap.get(CV_CAP_PROP_FRAME_COUNT);
	vid._percentVideoPerFrame = 1.0 / vid._duration;

	for(;;)
	{
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

		performGlobalMatching(initialImage);
	}
	cv::waitKey(0);
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


void performGlobalMatching(Mat initialImage) {
	/*First of all we look for possible matches based on the colour of the wasp's ids.
	The waspsTest list of wasps is refreshed with the new info.*/
	previousIdsDetection(initialImage);

	/* Now we check the potential results by finding orientation of the suggested wasps.
	If no result is given for a certain wasp, it is deleted from the list.*/
	
	checkWaspsOrientation(initialImage);
	
	//Seria aqui la llamada a la funcion de deteccion de los cuerpos?
}


void previousIdsDetection(Mat initialImage) {
	namedWindow("video", 1);
	int erosionSize = 1;
	int erosionType = 2;
	int thresh = 50;
	int max_thresh = 100;
	RNG rng(12345);
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	cv::Mat image, splitedImages, previous, ids, drawing, channel[3];
	
	//findAndSetColor(initialImage, 'w', splitedImages);
	//ids = splitedImages;
	findAndSetColor(initialImage, 'g', splitedImages);
	ids = splitedImages;
	findAndSetColor(initialImage, 'b', splitedImages);
	ids = ids + splitedImages;
	findAndSetColor(initialImage, 'r', splitedImages);
	ids = ids + splitedImages;
	findAndSetColor(initialImage, 'y', splitedImages);
	ids = ids + splitedImages;
	findAndSetColor(initialImage, 'p', splitedImages);
	ids = ids + splitedImages;
	findAndSetColor(initialImage, 'c', splitedImages);
	ids = ids + splitedImages;

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
	// We save the original image with the previous results before applying philters.
	previous = ids.clone();
	namedWindow("test", 1);
	/* We blur the result image so that the nearby results (usually belonging to the same wasp)
	get merged.*/
	blur( ids, ids, Size( erosionSize*5, erosionSize*5 ), Point(-1,-1) );
	imshow("test", ids);
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
	vid._camDist = diametroMayorEtiqueta(ids);
	
	// We merge the detected nearby wasps to just one
	mergeNearbyIds(contours, mc);

	/// Draw contours
	Wasp* test;
	int wasp = 0;
	drawing = initialImage;
	split(ids, channel);
 	waspsListTest = WaspList();
	cout << "contours " << contours.size() << endl;
	for( int i = 0; i < contours.size(); i++ )
	{
		cout << "hola";
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
	
	newWaspNumber = wasp;
	cout << wasp;
	
	imshow("video", drawing);
	cv::waitKey(0);
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
	
	
	//Si no hay avispas no hacemos nada
	if(newWaspNumber == 0)
		return;
		
	// 1. Miramos si el numero de avispas en la imagen ha cambiado
	if(waspNumber != newWaspNumber) {
		if(vid._camDist > biggestContour)
			biggestContour = vid._camDist;
	}
	
	//Imagen que mostraremos con los cuerpos
	Mat imagenResultado = img;
	//2. Recorremos las avispas para sacar el cuerpo
	for(int i = 0; i < waspsListTest.getSize(); i++) {
	
		Rect rectangulo = dameRectanguloRecorte(waspsListTest.getWaspFromPos(i)->_x, waspsListTest.getWaspFromPos(i)->_y, imagenResultado, biggestContour);
	
		Mat recorte;
		img(rectangulo).copyTo(recorte);
		
		//sacamos los radianes de inclinacion
		float rads = getBodyOrientation(recorte);
		
		//pintamos la linea
		//sacamos el punto final de la linea
		float longitud = biggestContour * 3.5;
		
		Point p = puntoFinalLinea(waspsListTest.getWaspFromPos(i)->_x, waspsListTest.getWaspFromPos(i)->_y, imagenResultado, longitud, rads);
		Point etiqueta(waspsListTest.getWaspFromPos(i)->_x, waspsListTest.getWaspFromPos(i)->_y);
		
		//3. Pintamos la linea del cuerpo en la imagen que se va a mostrar luego
		line(imagenResultado, p, etiqueta, Scalar(255,0,0), 10, 8, 0);
	}
	
	namedWindow("cuerpo", 1);
	imshow("cuerpo", imagenResultado);
	
	
	
}

float getBodyOrientation(Mat img) {
	
	float score = 2550;
	Point best;
	float bestAngle;
	float bestRadian = -1;
	float distSmall = 20;
	Mat bimg, gimg, rimg;
	
	Point central(img.size().width / 2, img.size().height / 2);
	
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
		double ladist = abs(media[0] - 24) + abs(media[1] - 16) + abs(media[2] - 29);
		if( ladist < score) {
			bestRadian = rad;
			bestAngle = gr;
			best = p;
			score = ladist;
			bimg = aux;
		}
	}
	
	return bestRadian;


}

Rect dameRectanguloRecorte(int x, int y, Mat img, float contArea) {
	//Sacamos el ancho y el alto en funcion del tamaño de la etiqueta
	float wihe = contArea * 3.5;
	int left, top;
	
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
		top = y - wihe;
	}
	
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
