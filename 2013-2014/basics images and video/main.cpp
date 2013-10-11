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
	
	cout << "Introduce un comando para seleccionar el ejemplo que quieres ejecutar" << endl;
	cin >> example;
	
	switch (example) {
		case 1:
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
			waitKey(0);                                          // Wait for a keystroke in the window
		break;
		case 2:
			cv::VideoCapture cap;
			int tbPos;
			const int alpha_slider_max = 100;
			int alpha_slider = 1;
			double alpha;
			double beta;
			Mat frame, blur;
			string tb;
			
			tb = "tb1";
			
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
		
    return 0;
}

void dummy(int, void *) {
	
}