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
	Mat img = imread("multimedia/images/prueba1.jpg");
	cerr << img.type();
	//Mat hsv;
	//cvtColor(img, hsv, COLOR_BGR2HSV);
	//blur(img,img,Size(5,5),Point(-1,-1),1);
	//namedWindow("imgOriginal",1);
	namedWindow("t",1);
	
	//TODO crear a como gray y pasar img a gray antes, asi no se repite tantas veces en el bucle
	cerr << "elgray: " << CV_BGR2GRAY << endl;
	
	//get the point of the center
	//TODO habria que restarel tema del diametro de la etiqueta, pero de momento no.
	Point center(img.size().width / 2, img.size().height / 2);
	
	float score = 2550;
	Point best;
	float bestAngle;
	float distSmall = 20;
	Mat bimg, gimg, rimg;
	
	//Bucle de grados en los que inclinar la linea
	for(float gr = 0; gr < 360; gr += 1) {
		float rad = gr * 0.0174532925;
		float dist = img.size().width / 2;
		Point p(dist * cos(rad) + dist , dist * sin(rad) + dist);
		Point ps(distSmall * cos(rad) + dist , distSmall * sin(rad) + dist);
		//creamos una imagen entera negra
		Mat a = Mat::zeros(img.size(), 16);
		//a.setTo(Scalar(15,15,30));
		line(a, p, ps, Scalar(255,255,255), 15, 8, 0);
		Mat aux = img & a;
		//cvtColor(aux, aux, CV_BGR2GRAY);
		//separamos en los 3 canales
		//cvSplit(aux, bimg, gimg, rimg);
		
		
		//inRange
		Mat asd;
		inRange(aux, Scalar(0,0,0), Scalar(1,1,1),asd);
		aux.setTo(Scalar(15,15,30),asd);
		
		
		Scalar media = mean(aux);
		double ladist = abs(media[0] - 15) + abs(media[1] - 15) + abs(media[2] - 30);
		cerr << gr << ": " << media << " --- " << ladist << endl;
		if( ladist < score) {
			bestAngle = gr;
			best = p;
			score = ladist;
			bimg = aux;
		}
		
		//circle(img, p, 1, Scalar(0,255,0), 1, 8, 0);
		//circle(img, ps, 1, Scalar(0,0,255), 1, 8, 0);
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
	//cerr << best << endl;
	cerr << bestAngle << endl;
	line(img, best, center, Scalar(255,0,0), 1, 8, 0);

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
	resize(img, img, Size(), 3, 3, INTER_CUBIC);
	//resize(hsv, hsv, Size(), 3, 3, INTER_CUBIC);
	imshow("t",img);
	//imshow("imgOriginal",a);

	waitKey(0);


};
