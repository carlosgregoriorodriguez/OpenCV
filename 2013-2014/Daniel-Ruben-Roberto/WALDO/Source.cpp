#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>

using namespace cv;
using namespace std;



int main(int argc, char* argv[])
{
	cv::Mat src_img, template_img;
	cv::Mat result_mat;
	cv::Mat debug_img;

	template_img = cv::imread("images/waldo1.png", CV_LOAD_IMAGE_GRAYSCALE);
	if (template_img.data == NULL) {
		printf("cv::imread() failed...\n");
		return -1;
	}

	src_img = cv::imread("images/image1.png", CV_LOAD_IMAGE_GRAYSCALE);
	if (src_img.data == NULL) {
		printf("cv::imread() failed...\n");
		return -1;
	}
	cv::cvtColor(src_img, debug_img, CV_GRAY2BGR);

	while (true) {
		// method: CV_TM_SQDIFF, CV_TM_SQDIFF_NORMED, CV_TM _CCORR, CV_TM_CCORR_NORMED, CV_TM_CCOEFF, CV_TM_CCOEFF_NORMED
		int match_method = CV_TM_CCORR_NORMED;
		cv::matchTemplate(src_img, template_img, result_mat, match_method);
		cv::normalize(result_mat, result_mat, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());

		double minVal; double maxVal;
		cv::Point minLoc, maxLoc, matchLoc;
		cv::minMaxLoc(result_mat, &minVal, &maxVal, &minLoc, &maxLoc, cv::Mat());
		if (match_method == CV_TM_SQDIFF || match_method == CV_TM_SQDIFF_NORMED)  
			matchLoc = minLoc;
		else matchLoc = maxLoc;

		cv::rectangle(
			debug_img,
			matchLoc,
			cv::Point(matchLoc.x + template_img.cols, matchLoc.y + template_img.rows),
			CV_RGB(255, 0, 0),
			3);

		cv::imshow("debug_img", debug_img);

		int c = cv::waitKey(1);
		if (c == 27) break; //tecla ESC
	}

	return 0;
}
