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
    Mat image;
	int example;
	
	cout << "Introduce un comando para seleccionar el ejemplo que quieres ejecutar:" << endl;
	cout << "1: Shows a picture with a hello world message." << endl;
	cout << "2: Shows your default webcam images and a trackbar to select the blur to be aplied." << endl;
	cout << "3: Shows the differences between two images by drawing circles." << endl;
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
			result = abs(img1-img2);
			
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
	}
		
    return 0;
}

void dummy(int, void *) {
	
}