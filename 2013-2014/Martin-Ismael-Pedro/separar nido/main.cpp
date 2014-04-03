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
#include <opencv2/contrib/contrib.hpp>
#include <stdio.h>

/*#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include "buscaobjetos.h"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/nonfree/features2d.hpp"
#include <stdio.h>*/



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
//Mat heatMap;
Mat previousFrame;
Mat blurred;
string tb = "tb1";
vector<Point> points;



Mat src, src_gray;
Mat dst, detected_edges;

int edgeThresh = 1;
int lowThreshold;
int const max_lowThreshold = 100;
int ratio = 3;
int kernel_size = 3;


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
void recorridodeavispa(Point point[], int numframes);
Rect separanido1(Mat second);
int separanido();
void CannyThreshold(int, void*);





int main( int argc, char** argv )
{
	int select;
	string numWasp = "";
	int idSize = 25;

	cout << "Insert numeric code for wasp detection method: " << endl;
	cout << "1: Detect wasps' ids." << endl;
	cout << "2: Movement detection among video frames" << endl;
	cout << "3: separar nido" << endl;
	cin >> select;
     //vector<Point> points1(100);
    Point points1[1000];
	switch(select) {
           
		case 1: {
            
			detectIds();
          
		}	
		break;
		case 2: {
			moveDetection();
		}
		case 3: {
			cout << "Introduce the number of the wasp to be followed: " << endl;
			cin >> numWasp;
			
            Mat recorrido(600, 600, CV_8UC3, Scalar(0));
            resize(recorrido, recorrido, Size(700, 550), 0, 0, INTER_CUBIC);
            //recorrido en captura de escena inicial
            Mat escena(600, 600, CV_8UC3, Scalar(0));
            resize(escena, escena, Size(700, 550), 0, 0, INTER_CUBIC);
            
            
            
			Mat tpl;
			Mat primer;
            Mat second;
			Point followedPoint = Point(-1, -1);
            Mat resta;

			int squareSize = 100;
			
			int error;
	
			initialize();
			
			cap.open("/Users/pedrete_142/Documents/proyectoprimeroopencv/proyectoprimeroopencv/multimedia/video/video.mts");
			namedWindow("video", 1);
            //namedWindow("body");
           
            vector<int> compression_params;
            compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);
        
			createTrackbar(tb, "video", &alpha_slider, alpha_slider_max, on_trackbar);
			cout << "first";
            int numframes=0;
			for(;;)
			{
                cout<<numframes<<"contadoeeeeeeeeer "<<endl;
                
				waitKey(20);
				if (frame.data) {
					previousFrame = frame.clone();
				}
              
                
				cap >> frame;
                if(numframes==0){
                    
                     resize(frame, frame, Size(700, 550), 0, 0, INTER_CUBIC);
                    primer = frame.clone();

                    imwrite( "/Users/pedrete_142/Documents/proyectoprimeroopencv/proyectoprimeroopencv/multimedia/images/esc.jpg", frame);
                }
                else if(numframes>=1){
                    
                resize(frame, frame, Size(700, 550), 0, 0, INTER_CUBIC);
                if(!frame.data)
				{
					printf("Error: no frame data.\n");
					break;
				}
				
				tbPos = getTrackbarPos(tb, "video");
                    if (numframes == 200) {
                        absdiff(primer, frame, second);
                        //resta=separanido1(second);
                        
                        frame(separanido1(second)).copyTo(resta);
                        
                    }
				if (tbPos <= 0)
					tbPos = 1;

				tpl = imread("/Users/pedrete_142/Documents/proyectoprimeroopencv/proyectoprimeroopencv/multimedia/images/" + numWasp + ".jpg", CV_32FC1);
				
				if (followedPoint.x < 0 || followedPoint.y < 0) {
					followedPoint = detectInterestPointFromTemplate(tpl);
				}
				else {
					followedPoint = followInterestPoint(frame, tpl, followedPoint, squareSize);
				}
				if (followedPoint.x >= 0 && followedPoint.y >= 0) {
					circle(frame, followedPoint, idSize, Scalar(0,250,0), 2, 8, 0);
				}
                    src=frame;
                    
                    
                    points1[numframes]=followedPoint;
                
				imshow("video", frame);
                
                waitKey(20);//valor por defecto 20
                if(numframes==201)
                    break;
			}
            numframes=numframes+1;
              
            }
           
            
           
            
            namedWindow("result");
            imshow("result", resta);
            waitKey(0);
            
		}
		break;
		default:
		break;
	}
	
    return 0;
	
}
Rect separanido1(Mat second){
    Mat second1;
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    vector<vector<Point> > contours1;
    vector<vector<Point> > mayor;
    vector<Vec4i> hierarchy1;
    

     cvtColor( second, second1 , CV_BGR2GRAY );
    
    
    
    blur( second1, detected_edges, Size(3,3) );
    
    /// Canny detector
    Canny( detected_edges, detected_edges, 99, 297, kernel_size );
    
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
     //Canny( drawing, drawing, 99, 297, kernel_size );
    findContours(drawing, contours1, hierarchy1, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
    double maxarea=0;
    int contourmax;
    for(int i=0;i<contours1.size();i++){
        if(contourArea(contours1[i])>maxarea){
            //contourmax=contours1[i];
            contourmax=i;
            maxarea=contourArea(contours1[i]);
        }
    }
   
        Scalar color = Scalar( 255, 255, 255 );
        drawContours( drawing, contours1, contourmax, color, 2, 8, hierarchy1, 0, Point() );
    Rect rectangulocontorno;
     cout<<"xxxxxxxxxxxxxxx"<<endl;
    //rectangulocontorno=fitEllipse(contours1[contourmax]);
    rectangulocontorno= boundingRect(contours1[contourmax]);
    
    cout<<"xxxxxxxxxxxxxxx"<<rectangulocontorno.x<<endl;
    cout<<"yyyyyyyyyyyyyyy"<<rectangulocontorno.y<<endl;
    //cout<<"yyyyyy"<<rectangulocontorno.y;
    Mat dest11;
    drawing(rectangulocontorno).copyTo(dest11);
    
    //}
   
    return rectangulocontorno;
    
}

void recorridodeavispa(Point point[], int numframes){
 
    Mat img;
    img = imread("/Users/pedrete_142/Documents/proyectoprimeroopencv/proyectoprimeroopencv/multimedia/images/esc.jpg");
    int r,g ,b;
    r=256;
    b=0;
    g=0;
    for(int i=1;i< numframes;i++){
        if(i<5){
            circle(img, point[i], 5, Scalar(250,250,250), 2, 8, 0);
        }
        else if(i>numframes-5){
            circle(img, point[i], 5, Scalar(250,0,0), 2, 8, 0);
        }
        else{
            
            circle(img, point[i], 5, Scalar(b,g,r), 2, 8, 0);
            
            
            /*if(r>0){
            if(i%10==0){
                r=r-1;
            }*/
            //}
            
            
            
            

        }
        
    }
    putText(img,"INICIO",Point(50,50),1,2,Scalar(255,255,255),2);
    putText(img,"FIN",Point(50,100),1,2,Scalar(255,0,0),2);
    imwrite("/Users/pedrete_142/Documents/proyectoprimeroopencv/proyectoprimeroopencv/multimedia/images/esc.jpg" ,img);
    
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

void detectIds() {
	/*namedWindow("adios",CV_WINDOW_NORMAL);
	namedWindow("hola",CV_WINDOW_NORMAL);
	int erosionSize = 1;
	int erosionType = 2;
	int thresh = 50;
	int max_thresh = 100;
	RNG rng(12345);
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	cv::Mat initialImage = cv::imread("/Users/pedrete_142/Documents/proyectoprimeroopencv/proyectoprimeroopencv/multimedia/images/wasps.jpg");
	cv::Mat channel[3];
	channel[0] = Mat::zeros(initialImage.rows, initialImage.cols, CV_BGR2GRAY);
	channel[1] = Mat::zeros(initialImage.rows, initialImage.cols, CV_BGR2GRAY);
	channel[2] = Mat::zeros(initialImage.rows, initialImage.cols, CV_BGR2GRAY);
	cv::Mat image;
	cv::Mat splitedImages[6];
	cv::Mat ids;
    
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
  findContours( canny, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );

  /// Get the moments
  vector<Moments> mu(contours.size() );
  for( int i = 0; i < contours.size(); i++ )
     { mu[i] = moments( contours[i], false ); }

  ///  Get the mass centers:
  vector<Point2f> mc( contours.size() );
  for( int i = 0; i < contours.size(); i++ )
     { mc[i] = Point2f( mu[i].m10/mu[i].m00 , mu[i].m01/mu[i].m00 ); }

  /// Draw contours
  Mat drawing = Mat::zeros( ids.size(), CV_8UC3 );
  split(ids, channel);
  for( int i = 1; i< contours.size(); i++ )
     {
		if (mc[i].x > 0) {
			cout << (int)channel[0].at<uchar>(mc[i].y, mc[i].x);
		   Scalar color = Scalar( (int)channel[0].at<uchar>(mc[i].y, mc[i].x), 
		   (int)channel[1].at<uchar>(mc[i].y, mc[i].x), 
		   (int)channel[2].at<uchar>(mc[i].y, mc[i].x));
		   //Scalar color = ids.at<uchar>(Point(mc[i].x, mc[i].y));
		   //drawContours( drawing, contours, i, color, 2, 8, hierarchy, 0, Point() );
		   circle( drawing, mc[i], 4, color, -1, 8, 0 );
       }
     }

  /// Show in a window
  namedWindow( "Contours", CV_WINDOW_AUTOSIZE );
  imshow( "Contours", drawing );

    
    cv::imshow("hola", ids);
    cv::imshow("adios", initialImage);
    cv::waitKey(0);
	
	
	*/
    
        namedWindow("adios",CV_WINDOW_NORMAL);
        namedWindow("hola",CV_WINDOW_NORMAL);
        int erosionSize = 1;
        int erosionType = 2;
        int thresh = 50;
        int max_thresh = 100;
        RNG rng(12345);
        vector<vector<Point> > contours;
        vector<Vec4i> hierarchy;
        cv::Mat initialImage = cv::imread("/Users/pedrete_142/Documents/proyectoprimeroopencv/proyectoprimeroopencv/multimedia/images/wasps.jpg");
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
        
        //Antes de aplicar canny, pasamos a binario la imagen
        cvtColor(ids, ids, CV_BGR2GRAY);
        threshold( ids, ids, 60, 255 ,THRESH_BINARY );
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
        }
        
        
        //Con contourArea
        cout << "++++ contourArea ++++" << endl;
        double best = 0;
        for( int i = 1; i < contours.size(); i++)
        {
            double asd = contourArea(contours[i]);
            if(asd > best)
                best = asd;
            cout << asd << endl;
        }
    cout << contours[1];
        
        //Sacamos el diametro del mejor contorno
        double diameter = sqrt(best / 3.1416) * 2;
        
        //Sacamos la proporcion entre la etiqueta y la pantalla
        double imageSize = (initialImage.rows + initialImage.cols) / 2;
        double prop = imageSize / diameter;
        
        cout << "////////////////////////" << endl;
        cout << "Mejor area: " << best << endl;	
        cout << "Dimension de imagen: " << imageSize << endl;
        cout << "Diagonal mejor area: " << diameter << endl;
        cout << "Proporcion: " << prop << endl;
        
        namedWindow("contornos",CV_WINDOW_NORMAL);
    cv:imshow("contornos", canny);
        cv::imshow("hola", ids);
        cv::imshow("adios", initialImage);
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
	cap.open("/Users/pedrete_142/Documents/proyectoprimeroopencv/proyectoprimeroopencv/multimedia/video/video.mts");
	
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