/* 
 * File:   main.cpp
 * Author: Daniel
 *
 * Created on 15 de diciembre de 2013, 18:47
 */

#include <cstdlib>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"


using namespace std;
using namespace cv;

/*
 * 
 */
int main(int argc, char** argv) {
    Mat img = imread("img/img4.jpg");
    cout << img.type() ;
    resize(img, img, (Size(612,384)));
    imshow("Original", img);
    //waitKey();
    Mat img_od = img.reshape(img.depth(),img.rows*img.cols);
    img_od.convertTo(img_od, CV_32F, 1./255);
    /*
     * Con K = 8 y epsilon 0.5 resultado interesante para las img1 e img2
     * Para la img5 hace falta, de momento, 1.15 de epsilon
     */
    int K = 8;
    Mat img_dst;
    Mat centers;
    //double kmeans(const Mat& samples, int clusterCount, Mat& labels, TermCriteria termcrit, int attempts, int flags, Mat* centers);
    kmeans(img_od,K
            ,img_dst,TermCriteria( CV_TERMCRIT_EPS+CV_TERMCRIT_ITER, 10, 4),3, KMEANS_PP_CENTERS, centers);
    //Mat final = img_dst;
    Mat final = img_dst.reshape(img.depth(), img.rows);
    final.convertTo(final, 16, 255.);
    //cvtColor(final,final,CV_YUV2BGR);
    imshow("Resultado", final);
    waitKey();
    return 0;
}

