#include <iostream>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "resta.h"

using namespace std;
using namespace cv;


/// Global Variables
int DELAY_CAPTION = 1500;
int DELAY_BLUR = 100;
int MAX_KERNEL_LENGTH = 31;
Mat src, src_gray;
Mat dst, detected_edges;

int edgeThresh = 1;
int lowThreshold;
int const max_lowThreshold = 100;
int ratio = 3;
int kernel_size = 3;

cv::Mat cargaImagen(String path) {
	cv::Mat img = imread(path, CV_LOAD_IMAGE_COLOR);
	return img;
}

void calculaDiferencias(String path1, String path2) {
	Mat img1, img1_gray;
	Mat img2, img2_gray;

	img1 = cargaImagen(path1);
	img2 = cargaImagen(path2);
	cvtColor(img1, img1_gray, CV_BGR2GRAY);
	cvtColor(img2, img2_gray, CV_BGR2GRAY);
	Mat result, resultCanny;
	result = abs(img1 - img2);
	double input;
	double alpha, beta;
	//    Mat bordes = cv::Mat::zeros(img1.rows, img1.cols,CV_32FC1);
	//    
	//    /// Ask the user enter alpha
	std::cout << " Simple Linear Blender " << std::endl;
	std::cout << "-----------------------" << std::endl;
	std::cout << "* Enter alpha [0-1]: ";
	std::cin >> input;
	//
	//    /// We use the alpha provided by the user if it is between 0 and 1
	if (input >= 0.0 && input <= 1.0) {
		alpha = input;
	}

	beta = (1.0 - alpha);
	//    
	//    cvtColor(result, result, CV_BGR2GRAY);
	//Canny(result, resultCanny, 80, 100);
	//    //bordes = bordes + result;
	//addWeighted(img2_gray, alpha, resultCanny, beta, 0.0, resultCanny);
	//    addWeighted(img2, alpha, bordes, beta, 0.0, result);
	//    /// Wait until user exit program by pressing a key

	imshow("Original1", img1);
	imshow("Original2", img2);


	const int alpha_slider_max = 100;
	int alpha_slider = 1;
	Mat resultBlur;
	string tb;
	int tbPos;

	tb = "tb1";

	//inicialmente vale 1
	int tbPosAux = 1;

	namedWindow("imagen resultado", 1);
	//Canny(result, resultCanny, 80, 100);
	createTrackbar(tb, "imagen resultado", &alpha_slider, alpha_slider_max, dummy);


	//mostramos la primera imagen del blur para el valor por defecto
	cv::blur(result, resultBlur, Size(1, 1), Point(-1, -1), BORDER_DEFAULT);
	Canny(resultBlur, resultBlur, 80, 100);
	addWeighted(img2_gray, alpha, resultBlur, beta, 0.0, resultBlur);
	imshow("imagen resultado", resultBlur);


	for (;;)
	{
		
		
		waitKey(20); // waits to display frame
		tbPos = getTrackbarPos(tb, "imagen resultado");

		if (tbPos <= 0)
			tbPos = 1;

		cv::blur(result, resultBlur, Size(tbPos, tbPos), Point(-1, -1), BORDER_DEFAULT);

		if (tbPosAux != tbPos){ //si hemos cambiado el valor del blur
			tbPosAux = tbPos;
			
			//sacar bordes
			Canny(resultBlur, resultBlur, 80, 100);

			//mezclar la imagen obtenida del canny con una de las originales
			addWeighted(img2_gray, alpha, resultBlur, beta, 0.0, resultBlur);

			imshow("imagen resultado", resultBlur);
		}

	}

	waitKey(0);
	
}

void dummy(int, void *) {

}
