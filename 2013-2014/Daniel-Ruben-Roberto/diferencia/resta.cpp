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

cv::Mat diferencia(cv::Mat img1, cv::Mat img2, int i) {
    GaussianBlur(img1, img1, Size(i, i), 0, 0);
    cv::Mat resultado = abs(img1 - img2);
    return resultado;
}

cv::Mat cargaImagen(String path) {
    cv::Mat img = imread(path, CV_LOAD_IMAGE_COLOR);
    return img;
}

void calculaDiferencias(String path1, String path2, int i) {
    Mat img1, img1_gray;
    Mat img2, img2_gray;

    img1 = cargaImagen(path1);
    img2 = cargaImagen(path2);
    cvtColor(img1, img1_gray, CV_BGR2GRAY);
    cvtColor(img2, img2_gray, CV_BGR2GRAY);
    Mat result;
    result = diferencia(img1_gray, img2_gray, i);
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
    Canny(result, result, 80, 100);
    //    //bordes = bordes + result;
    addWeighted(img2_gray, alpha, result, beta, 0.0, result);
    //    addWeighted(img2, alpha, bordes, beta, 0.0, result);
    //    /// Wait until user exit program by pressing a key

    imshow("Original1", img1);
    imshow("Original2", img2);
    imshow("Differs1", result);
    waitKey(0);
    //String file_path;
    //cout << "Output file path: ";
    //cin >> file_path;
    //imwrite(file_path, result);
}