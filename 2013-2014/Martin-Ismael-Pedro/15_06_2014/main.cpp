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

using namespace cv;
using namespace std;

class VideoWasps {
	public:
		double _camDist;
		double _camDistFactor;
		double _duration;
		double _percentVideoPerFrame;
		String _path;
		int _fps;
		VideoWasps() {
		    _camDistFactor = 2.0;
		}
};

//Number of wasp in screen
int waspNumber = 0;
int newWaspNumber;
int lastId = 0;
float biggestContour = 0;
int frameNum = 0;
Mat prevImg = Mat();
Mat restaImg = Mat();
Mat cadaDiez[20];
Mat colaFrames[20];

// Video initialization.
VideoWasps vid = VideoWasps();
cv::VideoCapture cap;

cv::Mat initialImage, splitedImages, frame, blurred, drawing, ids;

// Region of interest of the nest to be followed during the processing.
Rect roi;

void initialize();
int openVideo(int argc, string videoPath);
void detectIds();
void postProcesado();

// To check and set the characteristic colours in a pixel.
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

// Finding and setting characteristic colours in images.
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

// Operations related to the use of found wasps' identifiers.
double diametroMayorEtiqueta(Mat img);
void mergeNearbyIds(vector<vector<Point> > &contours, vector<Point2f> &mc);

// Matching of characteristic colours.
cv::Mat maskedImage(Mat id, Mat originalImage);
Mat maskedImageProcessing(Mat img);

// Operations with contours
vector<vector<Point> > getContoursWithCanny(Mat img, int cannyThres, int maxCannyThresh, int contType, int contWay);
vector<Point2f> getContoursMassCenters(vector<vector<Point> > contours);

// Step from local matching to a new global matching.
void compareLastLocalToGlobalMatching();

// Calculus with points
float distanceBetweenPoints(Point p1, Point p2);

// Selección del área de interés del nido
Rect separanido1(Mat second);
Rect separanidogeneral(string ruta);

//Deteccion del cuerpo
float getBodyOrientation(Mat img, Mat imgResta);
Rect dameRectanguloRecorte(int x, int y, Mat img, float contArea);
Point puntoFinalLinea(int x, int y, Mat img, float wihe, float rad);
void newMethodWaspsOrientation(Mat img);
int getWaspAngleByRotatedRect(RotatedRect rr, int w);
int getWaspAngleByColor(float x, float y, Mat img);
Point puntoFinalLineaNormal(int x, int y, Mat img, float distance, float rad);

class Wasp {
public:
	int _x;
	int _y;
	int _num;
	char _idColor;
	int _direction;
	int _wings;
	int _behaviour;
	Point _body;
	float _orientation;
	cv::Mat _heatMapPos;
    Vector<Point> patronrecorrido;
	bool _lost;
	bool _cambio;
	int _contour;
    
	Wasp(int x, int y, cv::Mat img) {
	_x = x;
	_y = y;
	_heatMapPos = cv::Mat(img.rows, img.cols, CV_64FC1, 0.0);
	
        _lost = false;
      

	}
	Wasp() {}
    
   
    void muestraPatronRecorrido(Mat img){
        namedWindow("patron de recorrido");
        Mat patron=cv::Mat(img.rows, img.cols, CV_8UC3, 0.0);
        cout<<"tamaño patron "<<patronrecorrido.size()<<endl;
        for(int i=0;i<patronrecorrido.size();i++){
            cout<<"valor "<<i <<patronrecorrido.operator[](i)<<endl;
            if(i<patronrecorrido.size()-(patronrecorrido.size()-1)){
                circle(patron, patronrecorrido.operator[](i), 15, Scalar(44,44,230), 2, 8, 0);
            }
            else if(i>patronrecorrido.size()-2){
                circle(patron, patronrecorrido.operator[](i), 15, Scalar(95,74,70), 2, 8, 0);
            }
            else{
                
                circle(patron, patronrecorrido.operator[](i), 3, Scalar(71,95,70), 2, 8, 0);
                
        }
        }
        putText(patron,"INICIO",Point(50,50),1,2,Scalar(44,44,230),2);
        putText(patron,"FIN",Point(50,100),1,2,Scalar(90,74,70),2);
        imshow("patron de recorrido", patron);
        waitKey(0);
    }
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
	vid._camDistFactor = 2.0;
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
	int dist = 300;
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
	tmp = distanceBetweenPoints(mc[i], Point(center, center));
	if (tmp < dist) {
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
	this->incrementHeatMap(Point(_x, _y));
                this->patronrecorrido.push_back(Point(_x,_y));
	}
	}
	}
    
	Point getPosition() {
	return Point(this->_x, this->_y);
	}
    
	Scalar getIdColor() {
	Scalar color;
	cout << "Avispa " << this->_num << " de color " << this->_idColor << endl;
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

class Node1 {
public:
    char _idColorwasp1;
    char _idColorwasp2;
    double time;
    Node1* _previous;
    Node1* _next;
    Node1(char idColorwasp1,char idColorwasp2,double time1) {
        _idColorwasp1=idColorwasp1;
        _idColorwasp2=idColorwasp2;
        time=time1;
    };
};
class relationship{
public:
    
    
    int _size;
    Node1* _first;
    
    
    relationship() {
        _first = NULL;
        _size = 0;
    }
    int getsize(){
        return _size;
    }
    void addRelation(char idcolorwasp1,char idcolorwasp2,double time) {
        Node1* node1 = new Node1(idcolorwasp1,idcolorwasp2,time);
        if (_size == 0) {
            _first = node1;
            _first->_next = NULL;
            _first->_previous = NULL;
            _size = _size + 1;
        }
        else {
            Node1* tmp = _first;
            _first = node1;
            _first->_previous = tmp;
            _first->_next = NULL;
            tmp->_next = _first;
            _size = _size + 1;
        }
    }
    int existrelationship(Wasp* wasp1,Wasp* wasp2){
        int existe=-1;
        int i=0;
        cout<<"idcolor avispa1"<<wasp1->getIdColor();
        cout<<"idcolor avispa2"<<wasp2->getIdColor();
        if(_size==0){
            existe=-1;
        }
        else{
            Node1* tmp = _first;
            while(tmp!=NULL && existe==-1){
               /* if((wasp1->getwordidcolor()==tmp->_idColorwasp1 && wasp2->getwordidcolor()==tmp->_idColorwasp2) || (wasp1->getwordidcolor()==tmp->_idColorwasp2 && wasp2->getwordidcolor()==tmp->_idColorwasp1)){
                    existe=i;
                    cout<<"eeeeeeeeeeeeeeeeeeeexiiiiiiiiissssssssssssste"<<endl;
                 */
                //
                //}
                if((wasp1->_idColor==tmp->_idColorwasp1 && wasp2->_idColor==tmp->_idColorwasp2)|| (wasp1->_idColor==tmp->_idColorwasp2 && wasp2->_idColor==tmp->_idColorwasp1)){
                    existe=i;
                }
                tmp=tmp->_previous;
                i++;
                
            }
        }
        return existe;
    }
    
    
    double gettimefrompos(int pos){
        Node1* tmp = _first;
        for (int i = _size - 1; i > pos; i--) {
            tmp = tmp->_previous;
        }
        return tmp->time;
    }
    
    void addTimeFromPos(int pos){
        Node1* tmp = _first;
        for (int i = _size - 1; i > pos; i--) {
            tmp = tmp->_previous;
        }
        tmp->time=tmp->time+vid._percentVideoPerFrame;
    }
    
    char getidcolor2fromPos(int pos){
        Node1* tmp = _first;
        for (int i = _size - 1; i > pos; i--) {
            tmp = tmp->_previous;
        }
        return tmp->_idColorwasp2;
    }
    char getidcolor1FromPos(int pos){
        Node1* tmp = _first;
        for (int i = _size - 1; i > pos; i--) {
            tmp = tmp->_previous;
        }
        return tmp->_idColorwasp1;
    }
    
    
};
// Methods or functions which need some of the data structures previusly created.
Wasp* coincidentWasp(Wasp * test);
int waspsSimillarity(Wasp *wasp1, Wasp* wasp2);
void performGlobalMatching();
void performLocalMatching();
void previousIdsDetection();
void checkWaspsOrientation(Mat img);
double calculamodulo(Wasp* w1, Wasp* w2);
void actualizatiempos();
void muestraporcentajesrelacion();

// Global dynamic array which keeps the info about the Wasps to be followed.
Wasp** wasps = new Wasp*[10];
Wasp** waspsTest = new Wasp*[10];
WaspList waspsList = WaspList();
WaspList waspsListTest = WaspList();
relationship relation= relationship();
int main( int argc, char** argv )
{
	vid._path = "multimedia/v2.MTS";
	roi = separanidogeneral(vid._path);
	//cout << roi.x << " " << roi.y << " " << roi.width << " " << roi.height;
    
	for(int f = 0; f < 19; f++)
	colaFrames[f] = Mat();
    
	waspsListTest = WaspList();
	waspsList = WaspList();
	detectIds();
}

void initialize() {
	frame = Mat();
	blurred = Mat();
	cap.open(vid._path);
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
		resize(frame, initialImage, Size(roi.height,roi.width), roi.y, roi.x, INTER_CUBIC);
		        if(frameNum==651){
		            waspsList.getWaspFromPos(5)->muestraPatronRecorrido(initialImage);
		        }
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
		        actualizatiempos();
		        //muestraporcentajesrelacion();
		cout << "frame " << frameNum << endl;
		imshow("video", drawing);
		imshow("test", ids);
		cv::waitKey(30);
		        
		        
		}
		//cv::waitKey(0);
	}
	//cv::waitKey(0);
    muestraporcentajesrelacion();
}
void muestraporcentajesrelacion(){
    for(int i=0;i<relation.getsize();i++){
        cout<<"----------------------------"<<endl;
        cout<<"relacion numero "<<i<<endl;
        cout<<"------COLOR AVISPA 1 "<<relation.getidcolor1FromPos(i)<<endl;
        cout<<"------COLOR AVISPA 2 "<<relation.getidcolor2fromPos(i)<<endl;
        cout<<"porcentaje de relacion "<<relation.gettimefrompos(i)*100<<"%"<<endl;
        cout<<"----------------------------"<<endl;
        
    }
}
void actualizatiempos(){
    for(int i=0;i<waspsList.getSize();i++){
        for(int j=i+1; j<waspsList.getSize();j++){
            Wasp* w1;
            Wasp* w2;
            w1=waspsList.getWaspFromPos(i);
            w2=waspsList.getWaspFromPos(j);
            double modulo= calculamodulo(w1,w2);
            //comprobar perdidas
            if((modulo>1 && modulo<100  ) && w1->_lost == false && w2->_lost==false){
                int pos=relation.existrelationship(w1, w2);
                if(pos!=-1){
                    relation.addTimeFromPos(pos);
                }
            }
            
        }
    }
}
double calculamodulo(Wasp* w1, Wasp* w2){
    int x1=w1->_x;
    int x2=w2->_x;
    int y1=w1->_y;
    int y2=w2->_y;
    double x=pow(double(x1-x2), 2);
    double y=pow(double(y1-y2),2);
    return sqrt(x+y);
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
	int distance = distanceBetweenPoints(mc[i], mc[j]);
	if (i != j && distance < vid._camDist) {
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
	distance = distanceBetweenPoints(Point(wasp1->_x, wasp1->_y), Point(wasp2->_x, wasp2->_y));
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
    
	newMethodWaspsOrientation(initialImage);
	postProcesado();
    
	//Mat hsv;
	//cvtColor(initialImage,hsv, COLOR_BGR2HSV);
	//Canny(hsv, hsv, 150, 200,3);
	//namedWindow("hsv",1);
	//imshow("hsv",hsv);
}

void performLocalMatching() {
	drawing = initialImage.clone();
	int listSize = waspsList.getSize();
	int lastCamFactor = vid._camDistFactor;
	vid._camDistFactor = 6.0;
	for (int i = 0; i < (int)listSize; i++) {
	if (!waspsList.getWaspFromPos(i)->_lost) {
	std::string numToString;
	std::stringstream out;
	out << waspsList.getWaspFromPos(i)->_num;
	numToString = out.str();
            
	waspsList.getWaspFromPos(i)->setNewPositionFromLastOne(initialImage);
	circle( drawing, Point(waspsList.getWaspFromPos(i)->_x, waspsList.getWaspFromPos(i)->_y), 4, waspsList.getWaspFromPos(i)->getIdColor(), -1, 8, 0 );
	cv::putText(drawing, numToString,
                        Point(waspsList.getWaspFromPos(i)->_x, waspsList.getWaspFromPos(i)->_y),
                        FONT_HERSHEY_COMPLEX_SMALL, 1, cvScalar(200,200,250), 1, CV_AA);
	}
	}
    
	newMethodWaspsOrientation(initialImage);
	postProcesado();
    
	vid._camDistFactor = lastCamFactor;
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
	vector<Point2f> mc;
    
	// Getting image with the colours of interest.
	ids = maskedImage(ids, initialImage);
	// Processing image
	ids = maskedImageProcessing(ids);
	// Getting contours from processed masked image
	contours = getContoursWithCanny(ids, 50, 100, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);
	// Getting mass centers for each contour
	mc = getContoursMassCenters(contours);
	// Here we calculate the camera distance
	vid._camDist = diametroMayorEtiqueta(ids);
    
	if (vid._camDist <= 0) {
	vid._camDist = 25;
	vid._camDistFactor = 2.0;
	}
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
	std::string numToString;
	std::stringstream out;
	int newIdNum = lastId;
	waspsListTest.addWasp(new Wasp(mc[i].x, mc[i].y, ids));
	//waspsTest[wasp] = new Wasp(mc[i].x, mc[i].y, ids);
	waspsListTest.getWaspFromPos(wasp)->setIdColor(ids);
	waspsListTest.getWaspFromPos(wasp)->_num = newIdNum;
	numToString = out.str();
	/*
                 circle( drawing, Point(waspsListTest.getWaspFromPos(wasp)->_x, waspsListTest.getWaspFromPos(wasp)->_y), 4, waspsListTest.getWaspFromPos(wasp)->getIdColor(), -1, 8, 0 );
                 cv::putText(drawing, numToString,
                 Point(waspsListTest.getWaspFromPos(wasp)->_x, waspsListTest.getWaspFromPos(wasp)->_y),
                 FONT_HERSHEY_COMPLEX_SMALL, 1, cvScalar(200,200,250), 1, CV_AA);
                 //waspsListTest.getWaspFromPos(wasp)->incrementHeatMap(Point(waspsListTest.getWaspFromPos(wasp)->_x,waspsListTest.getWaspFromPos(wasp)->_y));
                 */
	wasp++;
	lastId++;
	}
	}
        for(int t=0;t<waspsListTest.getSize();t++){
            for(int j=t+1;j<waspsListTest.getSize();j++){
                if(relation.existrelationship(waspsListTest.getWaspFromPos(t), waspsListTest.getWaspFromPos(j))==-1){
                    
                    //añadir consigo mismo
                    relation.addRelation(waspsListTest.getWaspFromPos(t)->_idColor, waspsListTest.getWaspFromPos(j)->_idColor,0);
                    
                }
            }
        }
	}
    
	wasp = 0;
    
	if (waspsList.getSize() <= 0) {
	waspsList = waspsListTest;
	}
	else {
	compareLastLocalToGlobalMatching();
	}
    
    
	newWaspNumber = wasp;
}


void compareLastLocalToGlobalMatching() {
	int tmpDistance;
    
	for (int j = 0; j < waspsList.getSize(); j++) {
	waspsList.getWaspFromPos(j)->_cambio = false;
	}
    
	// Buscar avispas local y no perdidas que no existan en global y marcarlas como perdidas
	for (int j = 0; j < waspsList.getSize(); j++) {
	bool foundNearby = false;
	for (int i = 0; i < waspsListTest.getSize() && !foundNearby; i++) {
            
	tmpDistance = distanceBetweenPoints(waspsList.getWaspFromPos(j)->getPosition(),
                                                waspsListTest.getWaspFromPos(i)->getPosition());
	//tmpDistance = std::sqrt(double((waspsList.getWaspFromPos(j)->_x - waspsListTest.getWaspFromPos(i)->_x)*(waspsList.getWaspFromPos(j)->_x - waspsListTest.getWaspFromPos(i)->_x)+(waspsList.getWaspFromPos(j)->_y - waspsListTest.getWaspFromPos(i)->_y)*(waspsList.getWaspFromPos(j)->_y - waspsListTest.getWaspFromPos(i)->_y)));
	if (tmpDistance < vid._camDist &&
                waspsList.getWaspFromPos(j)->_idColor == waspsListTest.getWaspFromPos(i)->_idColor
                && !waspsList.getWaspFromPos(j)->_lost && !waspsList.getWaspFromPos(j)->_cambio) {
	foundNearby = true;
	cout << "Avispa " << waspsList.getWaspFromPos(j)->_num << " no perdida" << endl;
	}
	}
	if (!foundNearby) {
	if (!waspsList.getWaspFromPos(j)->_lost)
	waspsList.getWaspFromPos(j)->_cambio = true;
	waspsList.getWaspFromPos(j)->_lost = true;
            
	cout << "Avispa " << waspsList.getWaspFromPos(j)->_num << " perdida" << endl;
	}
        
	cout << "avispa " << waspsList.getWaspFromPos(j)->_num << " cambio " <<
	waspsList.getWaspFromPos(j)->_cambio << endl;
	}
    
    
	// Buscando avispas encontradas en el global que encajen con las que hay
	// en la lista local. Si encontramos resultado para perdida y para no perdida
	// prevalece el de la no perdida.
	//    si coincide con alguna, se pone en la local la posicion nueva
	//	  si no coincide con ninguna, se añade nueva avispa a la lista local
	for (int i = 0; i < waspsListTest.getSize(); i++) {
	bool foundNearby = false;
	bool foundNearbyLost = false;
	int foundPos = -1;
	int foundPosLost = -1;
	for (int j = 0; j < waspsList.getSize(); j++) {
	int finalDistance = 300;
	int finalDistanceLost = 300;
	tmpDistance = distanceBetweenPoints(waspsList.getWaspFromPos(j)->getPosition(),
                                                waspsListTest.getWaspFromPos(i)->getPosition());
	//tmpDistance = std::sqrt(double((waspsList.getWaspFromPos(j)->_x - waspsListTest.getWaspFromPos(i)->_x)*(waspsList.getWaspFromPos(j)->_x - waspsListTest.getWaspFromPos(i)->_x)+(waspsList.getWaspFromPos(j)->_y - waspsListTest.getWaspFromPos(i)->_y)*(waspsList.getWaspFromPos(j)->_y - waspsListTest.getWaspFromPos(i)->_y)));
	if (tmpDistance < vid._camDist && tmpDistance < finalDistance &&
                waspsList.getWaspFromPos(j)->_idColor == waspsListTest.getWaspFromPos(i)->_idColor
                && !waspsList.getWaspFromPos(j)->_lost && !waspsList.getWaspFromPos(j)->_cambio) {
	waspsList.getWaspFromPos(j)->_x = waspsListTest.getWaspFromPos(i)->_x;
	waspsList.getWaspFromPos(j)->_y = waspsListTest.getWaspFromPos(i)->_y;
	waspsList.getWaspFromPos(j)->_lost = false;
	waspsList.getWaspFromPos(j)->_cambio = true;
	foundNearby = true;
	foundPos = j;
	finalDistance = tmpDistance;
	cout << "Avispa " << waspsList.getWaspFromPos(j)->_num << " no perdida encontrada"
	<< " de color " << waspsList.getWaspFromPos(j)->_idColor << endl;
	}
	else if (tmpDistance < vid._camDist * vid._camDistFactor && tmpDistance < finalDistanceLost &&
                     waspsList.getWaspFromPos(j)->_idColor == waspsListTest.getWaspFromPos(i)->_idColor
                     && waspsList.getWaspFromPos(j)->_lost && !waspsList.getWaspFromPos(j)->_cambio) {
	waspsList.getWaspFromPos(j)->_x = waspsListTest.getWaspFromPos(i)->_x;
	waspsList.getWaspFromPos(j)->_y = waspsListTest.getWaspFromPos(i)->_y;
	waspsList.getWaspFromPos(j)->_lost = false;
	waspsList.getWaspFromPos(j)->_cambio = true;
	foundNearbyLost = true;
	foundPosLost = j;
	finalDistanceLost = tmpDistance;
	cout << "Avispa " << waspsList.getWaspFromPos(j)->_num << " perdida encontrada"
	<< " de color " << waspsList.getWaspFromPos(j)->_idColor << endl;
	}
	}
        
	if (!foundNearby && !foundNearbyLost) {
	cout << "Avispa " << waspsListTest.getWaspFromPos(i)->_num << " añadida"
	<< " de color " << waspsListTest.getWaspFromPos(i)->_idColor << endl;
	waspsList.addWasp(waspsListTest.getWaspFromPos(i));
	waspsList.getWaspFromPos(waspsList.getSize()-1)->_cambio = true;
	}
	}
	if (frameNum == 651)
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
        
        
	//sacamos los radianes de inclinacion
	float rads = getBodyOrientation(recorte, recorteResta);
        
	//pintamos la linea
	//sacamos el punto final de la linea
	float longitud = biggestContour * vid._camDistFactor;
        
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
	if (vid._camDistFactor <= 0) {
	vid._camDistFactor = 4.0;
	}
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
	float dist = img.size().width / 20 * vid._camDistFactor;
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

Rect separanidogeneral(string ruta){
	cv::VideoCapture cap1;
    cap1.open(ruta);
    Mat firstframe, frame, secondframe;
    Rect rect;
    
    for(int i=0;i<200;i++){
        
        cap1 >> frame;
        resize(frame, frame, Size(700, 550), 0, 0, INTER_CUBIC);
        if(i==0){
            
            firstframe = frame.clone();
            
        }
        
    }
    Mat salida;
    
    absdiff(firstframe, frame, secondframe);
    frame(separanido1(secondframe)).copyTo(salida);
    
    return separanido1(secondframe);
    
}

Rect separanido1(Mat second){
    Mat second1, detected_edges;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    vector<vector<Point> > contours1;
    vector<vector<Point> > mayor;
    vector<Vec4i> hierarchy1;
    
    cvtColor( second, second1 , CV_BGR2GRAY );
    //blur(second1, second1, Size(1,1));
    
    blur( second1, detected_edges, Size(3,3) );
    
    /// Canny detector
    Canny( detected_edges, detected_edges,10, 200, 3 );
    /// Find contours
    findContours( detected_edges, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
    
    /// Draw contours
    Mat drawing = Mat::zeros( detected_edges.size(), CV_8UC3 );
    
    for( int i = 0; i< contours.size(); i++ )
    {
        Scalar color = Scalar( 255, 255, 255 );
        drawContours( drawing, contours, i, color, 2, 8, hierarchy, 0, Point() );
    }
    
    blur( drawing, drawing, Size(80,80) );
    
    cvtColor( drawing, drawing , CV_BGR2GRAY );
    
    findContours(drawing, contours1, hierarchy1, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
    double maxarea=0;
    int contourmax;
    for(int i=0;i<contours1.size();i++){
        if(contourArea(contours1[i])>maxarea){
            contourmax=i;
            maxarea=contourArea(contours1[i]);
        }
    }
    
    Rect rectangulocontorno;
    //rectangulocontorno=fitEllipse(contours1[contourmax]);
    rectangulocontorno= boundingRect(contours1[contourmax]);
    
    return rectangulocontorno;
    
}



//////////////////////////////////////////
// Body orientation detection
//////////////////////////////////////////
void newMethodWaspsOrientation(Mat img) {
	/////////////////////////////////
	// Guardar 20 frames
	/////////////////////////////////
    
	//Guardamos la imagen actual para pintar sobre ela
	Mat imagenResultado = img.clone();
    
	//Si es el primer frame, metemos 20 iguales en la cola
	if(prevImg.empty()) {
	prevImg = img.clone();
	for(int f = 0; f < 20; f++) {
	colaFrames[f] = img.clone();
	}
	} else {
        //Si no es el primer frame, pusheamos la cola
        for(int f = 0; f < 19; f++)
            colaFrames[f] = colaFrames[f + 1].clone();
        
        colaFrames[19] = img.clone();
	}
    
	//Sacamos la resta entre el frame actual y el de hace 20
	Mat diferencia = Mat();
	diferencia = abs(colaFrames[19] - colaFrames[0]);
    
    
	//Aplicamos filtros sobre la imagen diferencia
	int erosionSize = 1;
	int erosionType = 2;
	Mat element = getStructuringElement(erosionType,
                                        Size(2*erosionSize + 1, 2*erosionSize+1),
                                        Point(erosionSize, erosionSize));
    
	//Serie de filtros sobre la imagen
	cvtColor(diferencia, diferencia, CV_BGR2GRAY);
	erode(diferencia, diferencia, element);
	threshold(diferencia, diferencia,20,255,0);
	erode(diferencia, diferencia, element);
	dilate(diferencia, diferencia, element );
	blur(diferencia, diferencia, Size(20, 20), Point(-1,-1) );
	blur(diferencia, diferencia, Size(erosionSize*5, erosionSize*5), Point(-1,-1));
	erode(diferencia, diferencia, element*5);
	threshold(diferencia, diferencia,1,255,0);
	blur(diferencia, diferencia, Size(20, 20), Point(-1,-1) );
	threshold(diferencia, diferencia,1,255,0);
	erode(diferencia, diferencia, element*8);
    
    
	////////////////////////////////
	//	  //
	//   Método por movimiento	  //
	//	  //
	////////////////////////////////
    
	//Sacamos los contornos
	Mat contornos = diferencia.clone();
    
	int thresh = 50;
	Canny( contornos, contornos, thresh, thresh*2, 3 );
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	findContours( contornos, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
    
	//Realizamos el primer bucle que asigna a cada avispa el contorno que la contiene
	for(int w = 0; w < waspsListTest.getSize(); w++) {
        
	//Inicializamos a -1 el contorno correspondiente
	waspsListTest.getWaspFromPos(w)->_contour = -1;
	for( int c = 0; c < contours.size(); c++)
	{
	if(contours[c].size() > 5) {
	RotatedRect el = fitEllipse(contours[c]);
	Rect rect = el.boundingRect();
                
	//TO-DO : utilizar el metodo contains en vez de esos if
                
	if(rect.contains(Point(waspsListTest.getWaspFromPos(w)->_x, waspsListTest.getWaspFromPos(w)->_y))) {
	waspsListTest.getWaspFromPos(w)->_contour = c;
	}
	}
	}
	}
    
	//Segundo bucle para reconocer si hay varias avispas con el mismo contorno asignado y asi asignarles contorno -1
	//Dentro del mismo bucle, si la avispa tiene un contorno distinto a -1, calculamos su ángulo por movimiento ó -1 si no es un rotated válido
	for(int w = 0; w < waspsListTest.getSize(); w++) {
        
	int con = waspsListTest.getWaspFromPos(w)->_contour;
        
	for(int w2 = w+1; w2 < waspsListTest.getSize() && con != -1; w2++) {
            
	if(waspsListTest.getWaspFromPos(w2)->_contour == con) {
	waspsListTest.getWaspFromPos(w)->_contour = -1;
	waspsListTest.getWaspFromPos(w2)->_contour = -1;
	}
	}
        
	//Sacamos el ángulo
	if(waspsListTest.getWaspFromPos(w)->_contour != -1)
	//waspsListTest.getWaspFromPos(w)->_direction = -1;
	waspsListTest.getWaspFromPos(w)->_direction = getWaspAngleByRotatedRect(fitEllipse(contours[waspsListTest.getWaspFromPos(w)->_contour]), w);
	else
	waspsListTest.getWaspFromPos(w)->_direction = -1;
	}
    
	//Tercer bucle, en el que miramos si una avispa tiene direction == -1 y si es asi calculamos su dirección por color
    
	//Sacamos el contorno mas grande
	if(vid._camDist > biggestContour)
        biggestContour = vid._camDist;
    
	Mat imgColor = img.clone();
	float longitud = 100;
    
	for(int w = 0; w < waspsListTest.getSize(); w++) {
        
	int dir = waspsListTest.getWaspFromPos(w)->_direction;
	float x = waspsListTest.getWaspFromPos(w)->_x;
	float y = waspsListTest.getWaspFromPos(w)->_y;
        
	Point etiqueta(x, y);
	Scalar color = Scalar(255,0,0);
        
	if(dir == -1) {
	Rect rectangulo = dameRectanguloRecorte(x, y, imgColor, biggestContour);
            
	waspsListTest.getWaspFromPos(w)->_direction = getWaspAngleByColor(x, y, imgColor(rectangulo));
            
	color = Scalar(0,255,0);
	}
        
	Point p = puntoFinalLineaNormal(x, y, img, longitud, waspsListTest.getWaspFromPos(w)->_direction * 0.0174532925);
        
	//3. Pintamos la linea del cuerpo en la imagen que se va a mostrar luego
	line(img, p, etiqueta, color, 10, 8, 0);
        
	}
    
    
	namedWindow("nuevooo",1);
	imshow("nuevooo",img);
}

int getWaspAngleByColor(float x, float y, Mat img) {
	//namedWindow("peque",1);
	float bestAngle;
	float bestRadian = -1;
	float score = 999999;
	Point best;
	Point central(img.size().width, img.size().width);
    
	for(float gr = 0; gr < 360; gr += 1) {
        
	float rad = gr * 0.0174532925;
	float dist = img.size().width / 20 * 8;
	float distSmall = img.size().width / 8;
        
	//Circulo grande donde acabaran las lineas
	Point p(dist * cos(rad) + img.size().width / 2 , -dist * sin(rad) + img.size().width / 2);
	//circulo pequeño para que la linea no coja la etiqueta
	Point ps(distSmall * cos(rad) + img.size().width / 2 , -distSmall * sin(rad) + img.size().width / 2);
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
	aux.setTo(Scalar(240,16,29),asd);
        
	//Sacamos la media y dista menos del marron que la actual nos quedamos con ella
	Scalar media = mean(aux);
	double ladist = abs(media[0] - 12) + abs(media[1] - 7) + abs(media[2] - 17);
	if( ladist < score) {
	bestRadian = rad;
	bestAngle = gr;
	best = p;
	score = ladist;
	//bimg = aux;
	}
	//imshow("peque",aux);
	//cout << "Angulo " << gr << " : " << ladist << endl;
        
	}
    
    
	return bestAngle;
    
}

int getWaspAngleByRotatedRect(RotatedRect rr, int w) {
    
	Rect rel = rr.boundingRect();
    
	float top = rel.y;
	float bot = rel.y + rel.height;
	float left = rel.x;
	float right = rel.x + rel.width;
    
	/**************************************************
     * Aqui miramos si el contorno es muy cuadrado, si lo es, devolvemos -1
     ***************************************************/
	int difMax = biggestContour;
	if(abs(abs(bot - top) - abs(right - left)) < difMax)
	return -1;
    
    
	//Si es agudo hacemos 90 - angulo, si es obtuso hacemos 180 - lo que abarque el angulo del segundo cuadrante
	int ang = static_cast<int>(rr.angle);
	if(ang < 90)
	ang = 90 - ang;
	else
	ang = 180 - (ang - 90);
    
	//Si la etiqueta está en la mitad superior, sumamos 180 al ángulo
	if( abs(top - waspsListTest.getWaspFromPos(w)->_y) < abs(bot - waspsListTest.getWaspFromPos(w)->_y) &&
       cos(ang * 0.0174532925) <= 0.76 && cos(ang * 0.0174532925) >= -0.76) {
	ang = ang + 180;
	ang = ang % 360;
	} 
	else if( abs(right - waspsListTest.getWaspFromPos(w)->_x) < abs(left - waspsListTest.getWaspFromPos(w)->_x) && cos(ang * 0.0174532925) > 0.76) {
	//Si la etiqueta está en la parte derecha y el angulo mira a la derecha, le damos la vuelta
	//cout << "der " << w << endl;
	ang = ang + 180;
	ang = ang % 360;
	} else if( abs(right - waspsListTest.getWaspFromPos(w)->_x) > abs(left - waspsListTest.getWaspFromPos(w)->_x) && cos(ang * 0.0174532925) < -0.76) {
	//Si la etiqueta está en la parte izquierda, miramos si hay que darle la vuelta, ¿Es esto necesario?
	//cout << "izq " << w << endl;
	ang = ang + 180;
	ang = ang % 360;
	}
    
    
	return ang;
}


Point puntoFinalLineaNormal(int x, int y, Mat img, float distance, float rad) {
    
	float left = distance * cos(rad) + x;
	if(left < 0 ) left = 0;
	if(left > img.size().width) left = img.size().width;
    
	float top = -(distance * sin(rad)) + y;
	if(top < 0) top = 0;
	if(top > img.size().height) top = img.size().height;
    
	Point ret(left,top);
    
	return ret;	
}
