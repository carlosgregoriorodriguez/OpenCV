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

using namespace cv;
using namespace std;

void dummy(int, void *);
void readme();

int main( int argc, char** argv )
{
    Mat image;
	int example;
	
	cout << "Introduce un comando para seleccionar el ejemplo que quieres ejecutar:" << endl;
	cout << "1: Shows a picture with a hello world message." << endl;
	cout << "2: Shows your default webcam images and a trackbar to select the blur to be aplied." << endl;
	cout << "3: Shows the differences between two images by drawing circles." << endl;
	cout << "4: Whitening and locally adaptive histogram ecualization." << endl;
	cout << "5: Where's Waldo?" << endl;
	cin >> example;
	
	switch (example) {
		case 1: {
			image = imread("multimedia/images/botin.jpg", CV_LOAD_IMAGE_COLOR);
			
			if(!image.data )                              // Check for invalid input
			{
				cout <<  "Could not open or find the image" << std::endl ;
				return -1;
			}
			
			// KEY LINE: Start the window thread
			//cvStartWindowThread();
			namedWindow("Display window", CV_WINDOW_AUTOSIZE );// Create a window for display.
			
			putText(image, "JELOU EVERIGUAN", cvPoint(100,120), FONT_HERSHEY_COMPLEX_SMALL, 0.8, Scalar::all(255), 1, 8);
			imshow("Display window", image);
			waitKey(0);  
		}                                        // Wait for a keystroke in the window
		break;
		case 2: {
			cv::VideoCapture cap;
			int tbPos;
			const int alpha_slider_max = 100;
			int alpha_slider = 1;
			double alpha;
			double beta;
			Mat frame = Mat();
			Mat blur = Mat();
			string tb = "tb1";
			
			if(argc > 1)
			{
				cap.open(string(argv[1]));
			}
			else
			{
				cap.open(CV_CAP_ANY);
			}
			if(!cap.isOpened())
			{
				printf("Error: could not load a camera or video.\n");
			}
		
			namedWindow("video", 1);
			
			createTrackbar(tb, "video", &alpha_slider, alpha_slider_max, dummy);
			for(;;)
			{
				waitKey(20);
				cap >> frame;
				if(!frame.data)
				{
					printf("Error: no frame data.\n");
					break;
				}

				blur = frame.clone();
				tbPos = getTrackbarPos(tb, "video");

				if (tbPos <= 0)
					tbPos = 1;
				cv::blur(frame, blur, Size(tbPos, tbPos), Point(-1, -1), BORDER_DEFAULT);
				imshow("video", blur);
			}
		}
		break;
		case 3: {
			Mat img1C, img1;
			Mat img2C, img2;
			Mat result;
			Mat final;
			Mat centers;
			vector<vector<Point>> contours;
			vector<Vec4i> hierarchy;

			//Reading data with grayscale format
			img1C = imread("multimedia/images/botin1.jpg");
			img2C = imread("multimedia/images/botin.jpg");
			
			//Operating with images
			cvtColor(img1C, img1, CV_BGR2GRAY);
			cvtColor(img2C, img2, CV_BGR2GRAY);
			cv::blur(img2, img2, Size(10, 10), Point(-1, -1), BORDER_DEFAULT);
			cv::blur(img1, img1, Size(10, 10), Point(-1, -1), BORDER_DEFAULT);
			result = abs(img2-img1);
			
			cv::blur(result, result, Size(10, 10), Point(-1, -1), BORDER_DEFAULT);
			threshold( result, result, 15, 255, 3);
			
			//Showing thresholded image
			namedWindow("threshold", 1);
			imshow("threshold", result);

			// Looking for independent contours within the thresholded substracted image.
			findContours(result, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));

			// Get the moments of the contours
			vector<Moments> mu(contours.size());
			for(int i = 0; i < contours.size(); i++) {
				mu[i] = moments(contours[i], false);
			}

			// Get the mass centers of the contours and their moments
			vector<Point2f> mc(contours.size());
			for(int i = 0; i < contours.size(); i++) {
				mc[i] = Point2f(mu[i].m10/mu[i].m00 , mu[i].m01/mu[i].m00); 
			}

			// Draw mass centers
			Mat drawing = Mat::zeros(result.size(), CV_8UC1);
			for( int i = 0; i< contours.size(); i++ ) {
				Scalar color = Scalar(255, 255, 255);
				line(drawing, mc[i], mc[i], color, 1, 8, 0);
			}
			
			//Showing mass centers of the thresholded substracted image.
			namedWindow("massCenters", 1);
			imshow("massCenters", drawing);
			
			// Drawing circles to mark the differences among the two initial images.
			final = img1C.clone();
			for (int i = 0; i < final.rows; i++) {
				for (int j = 0; j < final.cols; j++) {
					if (drawing.at<uchar>(i,j) > 0) {
						circle(final, Point(j, i), 25, Scalar(255,255,255), 1, 8, 0);
					}
				}
			}
			
			namedWindow("img1", 1);
			namedWindow("img2", 1);
			namedWindow("differences", 1);
			imshow("img1", img1C);
			imshow("img2", img2C);
			imshow("differences", final);
			
			waitKey(0); 
		break;
		}
		case 4: { 
			Mat img1C, img1, whitened1;
			Mat img2C, img2, whitened2;
			double mean1, mean2;
			double variance1, variance2;
			double substract;
			
			//Reading data with grayscale format
			img1C = imread("multimedia/images/botin1.jpg");
			img2C = imread("multimedia/images/botin2.jpg");
			
			//Operating with images
			cvtColor(img1C, img1, CV_BGR2GRAY);
			cvtColor(img2C, img2, CV_BGR2GRAY);
			
			mean1 = 0;
			mean2 = 0;
			variance1 = 0;
			variance2 = 0;
			//Calculating mean and variance
			for (int i = 0; i < img1.rows; i++) {
				for (int j = 0; j < img1.cols; j++) {
					mean1 = mean1 + (int)img1.at<uchar>(i,j);
					mean2 = mean2 + (int)img2.at<uchar>(i,j);
				}
			}
			mean1 = mean1 / (img1.rows * img1.cols);
			mean2 = mean2 / (img2.rows * img2.cols);
			
			for (int i = 0; i < img1.rows; i++) {
				for (int j = 0; j < img1.cols; j++) {
					variance1 = variance1 + ((int)img1.at<uchar>(i,j) - mean1) * ((int)img1.at<uchar>(i,j) - mean1);
					variance2 = variance2 + ((int)img2.at<uchar>(i,j) - mean2) * ((int)img2.at<uchar>(i,j) - mean2);
				}
			}
			variance1 = sqrt(variance1 / (img1.rows * img1.cols));
			variance2 = sqrt(variance2 / (img2.rows * img2.cols));
			cout << mean1 << " " << variance1 << endl << mean2 << " " << variance2;
			
			// Whitening
			whitened1 = img1.clone();
			whitened2 = img2.clone();
			for (int i = 0; i < img1.rows; i++) {
				for (int j = 0; j < img1.cols; j++) {
					substract = (double)((whitened1.at<uchar>(i,j) - mean1)/variance1);
					if (substract < 0) 
						substract = -substract;
					whitened1.at<uchar>(i,j) = (int)(substract * 255 / ((255-mean1) / variance1));

					substract = (double)(((int)whitened2.at<uchar>(i,j) - mean2)/variance2);
					if (substract < 0)
						substract = -substract;
					whitened2.at<uchar>(i,j) = (int)(substract * 255 / ((255-mean1) / variance1));
				}
			}
			
			namedWindow("img1", 1);
			namedWindow("img2", 1);
			imshow("img1", img1);
			imshow("img2", img2);
			
			
			namedWindow("whitened1", 1);
			namedWindow("whitened2", 1);
			imshow("whitened1", whitened1);
			imshow("whitened2", whitened2);

			waitKey(0);
		}
		break;
		case 5: { 
			Mat waldo, scene1, scene2, scene3, scores;
			Mat resizedWaldo;
			int resultRows , resultCols;
			int finalRows, finalCols;
			int param;
			double minVal; 
			double maxVal; 
			double finalVal = 0.00;
			Point minLoc; 
			Point maxLoc;
			Point matchLoc;
			Point finalLoc;
			
			
			waldo = imread("multimedia/images/waldo.jpg", CV_32FC1);
			scene1 = imread("multimedia/images/scene1.jpg", CV_32FC1);
			//scene1 = imread("multimedia/images/scene2.jpg", CV_32FC1);
			finalRows = waldo.rows;
			finalCols = waldo.cols;
			param = waldo.rows/6;
			for (int i = waldo.rows, j = waldo.cols, it = 0; i >= param; i = i - 3) {
				resize(waldo, resizedWaldo, Size(j, i), 0, 0, INTER_CUBIC);
				resultCols = scene1.cols - resizedWaldo.cols + 1;
				resultRows = scene1.rows - resizedWaldo.rows + 1;

				//scores.eye(resultRows, resultCols , CV_32FC1);
				scores.create(resultRows, resultCols, CV_32FC1);
				
				matchTemplate(scene1, resizedWaldo, scores, TM_CCORR_NORMED);
				//normalize( scores, scores, 0, 1, NORM_MINMAX, -1, Mat() );
				 /// Localizing the best match with minMaxLoc
				minMaxLoc( scores, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );
				
				/// For SQDIFF and SQDIFF_NORMED, the best matches are lower values. For all the other methods, the higher the better
			    
				//if( match_method  == CV_TM_SQDIFF || match_method == CV_TM_SQDIFF_NORMED )
				//{
				//	matchLoc = minLoc; 
				//}
				//else
				//{ 
				//	matchLoc = maxLoc;
				//}
				
				matchLoc = maxLoc;
				cout << maxVal<< endl;
				if (finalVal < maxVal) {
					finalVal = maxVal;
					finalLoc = matchLoc;
					finalRows = i;
					finalCols = j;
				}
				it++;
				j = waldo.cols - (double)waldo.cols / (double)waldo.rows * 3 * it;
			}	
			cout << finalLoc.x << " " << finalLoc.y;
			rectangle( scene1, finalLoc, Point( finalLoc.x + finalCols , finalLoc.y + finalRows ), Scalar(0,255,0), 2, 8, 0 );
			resize(scene1, scene1, Size(700, 550), 0, 0, INTER_CUBIC);
			namedWindow("scene1", 1);
			//namedWindow("scene2", 1);
			//namedWindow("scene3", 1);
			
			
			imshow("scene1", scene1);
			//imshow("scene2", scene2);
			//imshow("scene3", scene3);	
			waitKey(0);
			
			/*
			cv::Mat img1 = imread("multimedia/images/waldo_face.jpg");
			cv::Mat img2 = imread("multimedia/images/scene4.jpg");
			
			if( !img1.data || !img2.data )
			{ 
				std::cout<< " --(!) Error reading images " << std::endl; return -1; 
			}
			
			//-- Step 1: Detect the keypoints using SURF Detector
			int minHessian = 400;
			
			// detecting keypoints
			SurfFeatureDetector detector(minHessian);
			vector<KeyPoint> keypoints1, keypoints2;
			detector.detect(img1, keypoints1);
			detector.detect(img2, keypoints2);

			// computing descriptors
			SurfDescriptorExtractor extractor;
			Mat descriptors1, descriptors2;
			extractor.compute(img1, keypoints1, descriptors1);
			extractor.compute(img2, keypoints2, descriptors2);

			// matching descriptors
			BFMatcher matcher(NORM_L2);
			vector<DMatch> matches;
			matcher.match(descriptors1, descriptors2, matches);
			
			// drawing the results
			namedWindow("matches", 1);
			Mat img_matches;
			drawMatches(img1, keypoints1, img2, keypoints2, matches, img_matches);
			imshow("matches", img_matches);
			
			waitKey(0);
			*/
		}
		break;
	}
		
    return 0;
}

void dummy(int, void *) {
	
}

void readme()
 { std::cout << " Usage: ./SURF_FlannMatcher <img1> <img2>" << std::endl; }