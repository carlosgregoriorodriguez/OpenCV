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
	Mat img = imread("multimedia/images/prueba1.jpg");
	namedWindow("t",1);
	namedWindow("t2",1);
	
	//get the point of the center
	Point center(img.size().width / 2, img.size().height / 2);
	
	float score = 2550;
	Point best;
	float bestAngle;
	float bestRadian;
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
		cerr << gr << ": " << media << " --- " << ladist << endl;
		if( ladist < score) {
			bestAngle = gr;
			bestRadian = rad;
			best = p;
			score = ladist;
			bimg = aux;
		}
		
		circle(img, p, 1, Scalar(0,255,0), 1, 8, 0);
		circle(img, ps, 1, Scalar(0,0,255), 1, 8, 0);
	}

	cerr << bestAngle << endl;
	cerr << bestRadian << endl;
	line(img, best, center, Scalar(255,0,0), 10, 8, 0);

	//img.copyTo(img, a);
	resize(bimg, bimg, Size(), 3, 3, INTER_CUBIC);
	resize(img, img, Size(), 3, 3, INTER_CUBIC);
	//resize(hsv, hsv, Size(), 3, 3, INTER_CUBIC);
	imshow("t",bimg);
	imshow("t2",img);

	waitKey(0);


};