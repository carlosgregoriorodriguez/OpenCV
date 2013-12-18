#include "stdafx.h"
#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

int main( int argc, char** argv )
{
	Mat image, img_display;


	//Leemos la imagen
	img_display = imread("input.jpg", CV_32FC1);

	// Create windows
	namedWindow( "resultado", CV_WINDOW_AUTOSIZE );

	/// Source image to display
	//image.copyTo( img_display );

	unsigned char *input = (unsigned char*)(img_display.data);

	for(int i=0; i<img_display.cols; i++)      //img1->height=img21->height
    {
        for(int j=0; j < img_display.rows; j++)     //img1->width=img2->width
        {
			img_display.at<cv::Vec3b>(j,i)[0] = 0;

			/*
			if(img_display.at<cv::Vec3b>(j,i)[0] <= 0 || img_display.at<cv::Vec3b>(j,i)[0] > 330)
			{
				//cout << "b";
				img_display.at<cv::Vec3b>(j,i)[0] = 0;
			}

			if(img_display.at<cv::Vec3b>(j,i)[1] <= 0 || img_display.at<cv::Vec3b>(j,i)[1] > 330)
			{
				//cout << "g";
				img_display.at<cv::Vec3b>(j,i)[1] = 0;
			}

			if(img_display.at<cv::Vec3b>(j,i)[2] <= 0 || img_display.at<cv::Vec3b>(j,i)[2] > 330)
			{
				//cout << "r";
				img_display.at<cv::Vec3b>(j,i)[2] = 0;
			}
			*/

			if(img_display.at<cv::Vec3b>(j,i)[0] != 0 && img_display.at<cv::Vec3b>(j,i)[1] != 0 && img_display.at<cv::Vec3b>(j,i)[2] != 0)
				cout << "yeas";

			if(img_display.at<cv::Vec3b>(j,i)[0] == 0 || img_display.at<cv::Vec3b>(j,i)[1] == 0 || img_display.at<cv::Vec3b>(j,i)[2] == 0)
			{
				
				img_display.at<cv::Vec3b>(j,i)[0] = 0;
				img_display.at<cv::Vec3b>(j,i)[1] = 0;
				img_display.at<cv::Vec3b>(j,i)[2] = 0;
			}

                /*
            int b1 = input[img_display.step * j + i ] ;
			int g1 = input[img_display.step * j + i + 1];
			int r1 = input[img_display.step * j + i + 2];

			if(b1 < 200 || b1 > 230)
				b1 = 0;

			if(g1 < 200 || g1 > 230)
				g1 = 0;

			if(r1 < 200 || r1 > 230)
				r1 = 0;


			if(b1 == 0 || g1 == 0 || r1 == 0)
			{
				b1 = 0;
				g1 = 0;
				r1 = 0;
			}
			*/
		}
	}

	/*
	//Declare a vector of Mat
	vector<Mat> channels(3);
	// split img:
	split(img_display, channels);
	// get the channels (dont forget they follow BGR order in OpenCV)

	//threshold over ch1(to test)
	threshold( channels[0], channels[0], 200, 255,3 );
	threshold( channels[0], channels[0], 220, 255,4 );

	threshold( channels[1], channels[1], 200, 255,3 );
	threshold( channels[1], channels[1], 220, 255,4 );

	threshold( channels[2], channels[2], 200, 255,3 );
	threshold( channels[2], channels[2], 220, 255,4 );

	unsigned char *input1 = (unsigned char*)( channels[0].data);
	unsigned char *input2 = (unsigned char*)( channels[1].data);
	unsigned char *input3 = (unsigned char*)( channels[2].data);

	//Loop
	 for(int i=0; i<img_display.rows; i++)
     {
            for(int j=0; j<img_display.cols; j++)
            {
				 int b1 = input1[channels[0].step * j + i ] ;
				 int g1 = input2[channels[1].step * j + i + 1];
				 int r1 = input3[channels[2].step * j + i + 2];
				 if(!(b1 && g1 && r1))
				 {
					 b1 = 0;
					 g1 = 0;
					 r1 = 0;
				 }
			}
	 }

	merge(channels,img_display);
	
	*/
	imshow( "resultado", img_display );

	waitKey(0);
	
	return 0;

}