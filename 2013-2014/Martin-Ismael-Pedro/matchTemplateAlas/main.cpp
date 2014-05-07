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

int main( int argc, char** argv ) {
	//Mat img = imread("wasps.jpg");
	Mat img = imread("wasps.jpg");
	Mat alas = imread("naranja.jpg");
	Mat result1,result3,resultThreshold1,resultThreshold3;
	
	
	//matchTemplate de alas sobre img
	matchTemplate( img, alas, result1, 1);
	matchTemplate( img, alas, result3, 3);
	threshold( result1, resultThreshold1, 0.9, 1 ,THRESH_BINARY );
	threshold( result3, resultThreshold3, 0.9, 1 ,THRESH_BINARY );
	//pasarlo a binario con threshold
	//cvtColor(result, result, CV_BGR2GRAY);
	//threshold( result, result, 0.9, 1 ,THRESH_BINARY );
	//pasar erodes para quitar los pequeños y despues blur para mejor contorno
	// Quedarnos con aquellos contornos mayores que x
	//Mirar si estan entre min dist y max dist del centro
	//Si están entonces mirar si hay negro entre medias
	//Si hay 1 pues es el cuerpo, si hay 2 pues miramos entre esas 2 si está ahi el cuerpo
	//si hay mas de 2, mirar por pares y la que de mejor
	
	
	
	
	//resize(bimg, bimg, Size(), 3, 3, INTER_CUBIC);
	//resize(result, result, Size(), 3, 3, INTER_CUBIC);
	
	
	namedWindow("ImagenNormal",1);
	imshow("ImagenNormal",img);
	
	namedWindow("matchtemplate 1",1);
	imshow("matchtemplate 1",result1);
	
	namedWindow("matchtemplate 3",1);
	imshow("matchtemplate 3",result3);
	
	namedWindow("threshold 1",1);
	imshow("threshold 1",resultThreshold1);
	
	namedWindow("threshold 3",1);
	imshow("threshold 3",resultThreshold3);
	
	waitKey(0);


};
