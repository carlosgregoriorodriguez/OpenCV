#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;


void hls(Mat src);
void hvs(Mat src);
void luv(Mat src);

int main(int argc, char *argv[])
{
	
	cv::Mat src = cv::imread("multimedia/images/botin.jpg", -1);
	namedWindow("original", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("original", src);

	hls(src);
	hvs(src);
	luv(src);

	// otras representaciones como lab, YUV...


	waitKey(0);
	 
	return 0;
}


void hls(Mat src){

	//// HLS -
	cv::Mat hls;

	// Convert from Red-Green-Blue to Hue-Saturation-Luminance
	cv::cvtColor(src, hls, CV_RGB2HLS);

	vector<Mat> hlsChannels;
	cv::split(hls, hlsChannels);

	namedWindow("HLS", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("HLS", hls);
	namedWindow("hlsChannels 0", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("hlsChannels 0", hlsChannels[0]);
	namedWindow("hlsChannels 1", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("hlsChannels 1", hlsChannels[1]);
	namedWindow("hlsChannels 2", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("hlsChannels 2", hlsChannels[2]);


}
void hvs(Mat src){

	////// HVS - H - Hue, S - Saturation, V - Value
	cv::Mat hsv;
	// Convert from Red-Green-Blue to Hue-Saturation-Luminance
	cv::cvtColor(src, hsv, CV_RGB2HSV);

	vector<Mat> hsvChannels;
	cv::split(hsv, hsvChannels);

	namedWindow("HSV", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("HSV", hsv);
	namedWindow("hsvChannels 0", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("hsvChannels 0", hsvChannels[0]);
	namedWindow("hsvChannels 1", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("hsvChannels 1", hsvChannels[1]);
	namedWindow("hsvChannels 2", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("hsvChannels 2", hsvChannels[2]);


}
void luv(Mat src){

	
	cv::Mat luv;
	// Convert from Red-Green-Blue to Hue-Saturation-Luminance
	cv::cvtColor(src, luv, CV_RGB2Luv);

	vector<Mat> luvChannels;
	cv::split(luv, luvChannels);

	namedWindow("LUV", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("LUV", luv);
	namedWindow("luvChannels 0", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("luvChannels 0", luvChannels[0]);
	namedWindow("luvChannels 1", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("luvChannels 1", luvChannels[1]);
	namedWindow("luvChannels 2", CV_WINDOW_AUTOSIZE);// Create a window for display.
	imshow("luvChannels 2", luvChannels[2]);

}