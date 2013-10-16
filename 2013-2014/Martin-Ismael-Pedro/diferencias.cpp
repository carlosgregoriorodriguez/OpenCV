#include "stdafx.h"
#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

void dummy(int, void *);

int main( int argc, char** argv )
{
	//Vars
	Mat image1,image2;

	//Read both images
	image1 = imread("image1.jpg", CV_LOAD_IMAGE_COLOR);
	image2 = imread("image2.jpg", CV_LOAD_IMAGE_COLOR);

	unsigned char *input1 = (unsigned char*)(image1.data);
	unsigned char *input2 = (unsigned char*)(image2.data);
	
	// Check for invalid input
	if(!image1.data || !image2.data )
	{
		cout <<  "Could not open or find the image" << std::endl ;
		return -1;
	}

	for(int i=0; i<image1.rows; i++)      //img1->height=img21->height
	{
		for(int j=0; j<image1.cols; j++)     //img1->width=img2->width
		{
		
			int b1 = input1[image1.step * j + i ] ;
            int g1 = input1[image1.step * j + i + 1];
            int r1 = input1[image1.step * j + i + 2];

			int b2 = input2[image2.step * j + i ] ;
            int g2 = input2[image2.step * j + i + 1];
            int r2 = input2[image2.step * j + i + 2];


			if(b1 != b2) //Blue channel
				cout << "Diferente azul" << endl;

			if(g1 != g2) //Green channel
				cout << "Diferente verde" << endl;

			if(r1 != r2) //Red channel
				cout << "Diferente rojo" << endl;

			int asd;
			cin >> asd;

		}
	}
}