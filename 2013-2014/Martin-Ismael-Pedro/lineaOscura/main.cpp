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
	Mat lt, ltr, lr, lbr, lb, lbl, ll, ltl;
	Mat img = imread("multimedia/images/prueba2.jpg");
	
	//namedWindow("imgOriginal",1);
	namedWindow("t",1);
	
	//TODO crear a como gray y pasar img a gray antes, asi no se repite tantas veces en el bucle
	cerr << "elgray: " << CV_BGR2GRAY << endl;
	
	//get the point of the center
	//TODO habria que restarel tema del diametro de la etiqueta, pero de momento no.
	Point center(img.size().width / 2, img.size().height / 2);
	
	float score = 255;
	Point best;
	float bestAngle;
	//Bucle de grados en los que inclinar la linea
	for(float gr = 0; gr < 360; gr += 3) {
		float rad = gr * 0.0174532925;
		float dist = img.size().width / 2;
		Point p(dist * cos(rad) + dist , dist * sin(rad) + dist);
		//creamos una imagen entera negra
		Mat a = Mat::zeros(img.size(), 16);
		line(a, p, center, Scalar(255,255,255), 3, 8, 0);
		Mat aux = img & a;
		cvtColor(aux, aux, CV_BGR2GRAY);
		Scalar media = mean(aux);
		cerr << media[0] << endl;
		if(media[0] < score) {
			bestAngle = gr;
			best = p;
			score = media[0];
		}
		
		circle(img, p, 1, Scalar(0,255,0), 1, 8, 0);
		
	}
	/*
	//Creamos los puntos finales de la linea
	Point* ps = new Point[28];
	ps[0] = Point(0,0);
	ps[1] = Point(img.size().width / 7, 0);
	ps[2] = Point(2*img.size().width / 7, 0);
	ps[3] = Point(3*img.size().width / 7, 0);
	ps[4] = Point(4*img.size().width / 7, 0);
	ps[5] = Point(5*img.size().width / 7, 0);
	ps[6] = Point(6*img.size().width / 7, 0);
	ps[7] = Point(img.size().width, 0);

	ps[8] = Point(img.size().width,img.size().height / 7);
	ps[9] = Point(img.size().width,2*img.size().height / 7);
	ps[10] = Point(img.size().width,3*img.size().height / 7);
	ps[11] = Point(img.size().width,4*img.size().height / 7);
	ps[12] = Point(img.size().width,5*img.size().height / 7);
	ps[13] = Point(img.size().width,6*img.size().height / 7);
	ps[14] = Point(img.size().width,img.size().height);

	ps[15] = Point(6*img.size().width / 7,img.size().height);
	ps[16] = Point(5*img.size().width / 7,img.size().height);
	ps[17] = Point(4*img.size().width / 7,img.size().height);
	ps[18] = Point(3*img.size().width / 7,img.size().height);
	ps[19] = Point(2*img.size().width / 7,img.size().height);
	ps[20] = Point(img.size().width / 7,img.size().height);
	ps[21] = Point(0,img.size().height);

	ps[22] = Point(0,6*img.size().height / 7);
	ps[23] = Point(0,5*img.size().height / 7);
	ps[24] = Point(0,4*img.size().height / 7);
	ps[25] = Point(0,3*img.size().height / 7);
	ps[26] = Point(0,2*img.size().height / 7);
	ps[27] = Point(0,img.size().height / 7);


	//Bucle para recorrer el array e ir quedándonos con la mejor
	float score = 255;
	int best = -1;
	for(int i = 0; i < 28; i++) {
		//creamos una imagen entera negra
		Mat a = Mat::zeros(img.size(), 16);
		line(a, ps[i], center, Scalar(255,255,255), 3, 8, 0);
		Mat aux = img & a;
		cvtColor(aux, aux, CV_BGR2GRAY);
		Scalar media = mean(aux);
		cerr << media[0] << endl;
		if(media[0] < score) {
			best = i;
			score = media[0];
		}
	}
	*/
	cerr << best << endl;
	cerr << bestAngle << endl;
	line(img, best, center, Scalar(255,0,0), 6, 8, 0);

/*
	// Al final del bucle pintamos la recta mejor


	//pintamos la linea sobre la imagen negra
	line(a, Point(400,0), center, Scalar(255,255,255), 3, 8, 0);

	//Recortamos donde la linea
	img = img & a;

	//Pasamos a escala de grises
	cvtColor(img, img, CV_BGR2GRAY);

	//Sacamos la media
	Scalar media = mean(img);

	cerr << media[0];
*/
	//img.copyTo(img, a);
	imshow("t",img);
	//imshow("imgOriginal",a);

	waitKey(0);


};
