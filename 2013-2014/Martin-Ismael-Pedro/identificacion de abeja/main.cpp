

#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include "buscaobjetos.h"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/nonfree/features2d.hpp"
#include <stdio.h>

using namespace cv;
using namespace std;

Mat edges;
Mat frame;
Mat frame1;
Mat treshold;
vector<Mat> bgr_planes;

int min_th=0;
int max_th=256;


int min_ts=0;
int max_ts=256;


int min_tv=0;
int max_tv=256;


const int FRAME_WIDTH = 640;
const int FRAME_HEIGHT = 480;

const int MAX_NUM_OBJECTS=50;

const int MIN_OBJECT_AREA = 20*20;
const int MAX_OBJECT_AREA = FRAME_HEIGHT*FRAME_WIDTH/1.5;


void on_trackbar(int valor,void*){
    threshold(bgr_planes[0], bgr_planes[0], min_th,max_th , 0);
   
    threshold(bgr_planes[1], bgr_planes[1], min_ts,max_ts , 0);
    
    threshold(bgr_planes[2], bgr_planes[2], min_tv,max_tv , 0);
}

void morphOps(Mat &thresh){
    /*función mas que nada para hacer más grande y claro una vez que aplicamos el trheshold y  que sea mas facil identificarlo, */
	//configuracion del KERNEL
    //MORPH_RECT estrutura rectangular
    /*getStructuringElement devuelve una estructura con el tamaño y la morfología que queremos mas o menos que se hagan las operaciones dilate y erode.*/
	Mat erodeElement = getStructuringElement( MORPH_RECT,Size(3,3));
    
   
	Mat dilateElement = getStructuringElement( MORPH_RECT,Size(11,11));
    
	erode(thresh,thresh,erodeElement);
	erode(thresh,thresh,erodeElement);
    
    
	dilate(thresh,thresh,dilateElement);
	dilate(thresh,thresh,dilateElement);
}
void drawObject(int x, int y,Mat &frame){
    

    
	circle(frame,Point(x,y),20,Scalar(0,255,0),2);
    if(y-25>0)
        line(frame,Point(x,y),Point(x,y-25),Scalar(0,255,0),2);
    else line(frame,Point(x,y),Point(x,0),Scalar(0,255,0),2);
    if(y+25<FRAME_HEIGHT)
        line(frame,Point(x,y),Point(x,y+25),Scalar(0,255,0),2);
    else line(frame,Point(x,y),Point(x,FRAME_HEIGHT),Scalar(0,255,0),2);
    if(x-25>0)
        line(frame,Point(x,y),Point(x-25,y),Scalar(0,255,0),2);
    else line(frame,Point(x,y),Point(0,y),Scalar(0,255,0),2);
    if(x+25<FRAME_WIDTH)
        line(frame,Point(x,y),Point(x+25,y),Scalar(0,255,0),2);
    else line(frame,Point(x,y),Point(FRAME_WIDTH,y),Scalar(0,255,0),2);
    
	
    
}
void trackFilteredObject(int &x, int &y, Mat threshold, Mat &cameraFeed){
    
	Mat temp;
	threshold.copyTo(temp);
	
    //venctor de los puntos del contorno
   
	vector< vector<Point> > contours;
    
     //vector con la jerarquía
    
	vector<Vec4i> hierarchy;
	
   
    //CV_RETR_CCOMP disttribuye los contornos en dos niveles
    //CV_chain_aprrox_simple para que me de los menos puntos posibles.
	findContours(temp,contours,hierarchy,CV_RETR_CCOMP,CV_CHAIN_APPROX_SIMPLE );
	//use moments method to find our filtered object
	double refArea = 0;
	bool objectFound = false;
	if (hierarchy.size() > 0) {
		int numObjects = hierarchy.size();
        //si el numero de objetos es mayor que MAX_NUM_OBJECTS tenemos ruido
       
        if(numObjects<MAX_NUM_OBJECTS){
            //recorre los contornos
            //la condicion es >=0 por que si el hierarchy[index][0] da negativo es que no hay siguiente contorno
			for (int index = 0; index >= 0; index = hierarchy[index][0]) {
                
				Moments moment = moments((cv::Mat)contours[index]);
				double area = moment.m00;
                //si el area es menor q 20 por 20 pixeles lo considero ruido
                //si el are es el mismo a 3/2 de la foto , es demasiado grande y no lo contamos
				//nosotros solo queremos el area mas grande. Asique vamos comparando
				
                if(area>MIN_OBJECT_AREA && area<MAX_OBJECT_AREA && area>refArea){
					x = moment.m10/area;
					y = moment.m01/area;
					objectFound = true;
					refArea = area;
				}else objectFound = false;
                
                
			}
                if(objectFound ==true){
				putText(cameraFeed,"ENCONTRADO",Point(0,50),2,1,Scalar(0,255,0),2);
				
				drawObject(x,y,cameraFeed);}
            
		}else putText(cameraFeed,"MUCHO RUIDO",Point(0,50),1,2,Scalar(0,0,255),2);
	}
}



int main (int argc, char *argv[])
{
    int x=0;
    int y=0;
    VideoCapture cap ("/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/fragmento_84.avi");  // Open the file
    
    if (!cap.isOpened ())               // Check if opening was successful
                    cerr << "I have failed!" << endl;
    
    else{
        
        namedWindow("edges",WINDOW_AUTOSIZE);
        
        namedWindow("frame",WINDOW_AUTOSIZE);
        createTrackbar("threshold min h", "edges",&min_th, max_th,on_trackbar);
        createTrackbar("threshold max h", "edges",&max_th, max_th,on_trackbar);
        
        createTrackbar("threshold min s", "edges",&min_ts, max_ts,on_trackbar);
        createTrackbar("threshold max s", "edges",&max_ts, max_ts,on_trackbar);
        
        createTrackbar("threshold min v", "edges",&min_tv, max_tv,on_trackbar);
        createTrackbar("threshold max v", "edges",&max_tv, max_tv,on_trackbar);
        

        while (cap.read (frame)){
            

            blur(frame, frame, Size(1,1));
            cvtColor(frame, frame1, CV_BGR2HSV);
            inRange(frame1,Scalar(min_th,min_ts,min_tv),Scalar(max_th,max_ts,max_tv),treshold);
            
            split( frame1, bgr_planes );
            on_trackbar(min_th, 0 );
            on_trackbar( max_th, 0 );
            
            on_trackbar(min_ts, 0 );
            on_trackbar( max_ts, 0 );
            
            on_trackbar(min_tv, 0 );
            on_trackbar( max_tv, 0 );
            merge(bgr_planes,  frame1);
            morphOps(treshold);
            trackFilteredObject(x,y,treshold,frame);
            imshow("edges", treshold);
            imshow("frame", frame);
            if(waitKey(30) >= 0) break;
        }
    }
    return 0;
}




