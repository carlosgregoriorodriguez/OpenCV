#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;


int main( int argc, char** argv ) {

    // Create the necessary matrices
    Mat src, dst;

    /// Load image
    src = imread("/home/ruben/OpenCV/images/botin.jpg", 1 );

    // Load the source image
    if( !src.data ) {
        cout << "Error al leer la imagen" << endl;
        return -1;
    }

    /// Separate the image in 3 places ( B, G and R )
    vector<Mat> bgr_planes;
    // Divides a multi-channel array into several single-channel arrays
    split( src, bgr_planes );

    /// Establish the number of bins
    int histSize = 256; //from 0 to 255 because B, G and R planes

    /// Set the ranges of values ( for B,G,R) )
    float range[] = { 0, 256 } ; //the upper boundary is exclusive
    const float* histRange = { range };

    // Make the bins to have the same size
    bool uniform = true;

    // Clear the histograms in the beginning
    bool accumulate = false;

    // Mat objects to save the histograms
    Mat b_hist, g_hist, r_hist;

    /// Compute the histograms:
    /* void calcHist(const Mat* images, int nimages, const int* channels, InputArray mask, OutputArray hist,
        int dims, const int* histSize, const float** ranges, bool uniform=true, bool accumulate=false ) */
    calcHist( &bgr_planes[0], 1, 0, Mat(), b_hist, 1, &histSize, &histRange, uniform, accumulate );
    calcHist( &bgr_planes[1], 1, 0, Mat(), g_hist, 1, &histSize, &histRange, uniform, accumulate );
    calcHist( &bgr_planes[2], 1, 0, Mat(), r_hist, 1, &histSize, &histRange, uniform, accumulate );

    // Draw the histograms for B, G and R
    int hist_w = 512; int hist_h = 400;
    int bin_w = cvRound( (double) hist_w/histSize );

    Mat histImage( hist_h, hist_w, CV_8UC3, Scalar( 0,0,0) );

    // Normalize the histogram so its values fall in the range indicated by the parameters entered
    /// Normalize the result to [ 0, histImage.rows ]
    // void normalize(const SparseMat& src, SparseMat& dst, double alpha, int normType)
    normalize(b_hist, b_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat() );
    normalize(g_hist, g_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat() );
    normalize(r_hist, r_hist, 0, histImage.rows, NORM_MINMAX, -1, Mat() );

    /// Draw for each channel
    // 1D-Histogram
    for( int i = 1; i < histSize; i++ ) {

        line( histImage, Point( bin_w*(i-1), hist_h - cvRound(b_hist.at<float>(i-1)) ) ,
                       Point( bin_w*(i), hist_h - cvRound(b_hist.at<float>(i)) ),
                       Scalar( 255, 0, 0), 2, 8, 0  );
        line( histImage, Point( bin_w*(i-1), hist_h - cvRound(g_hist.at<float>(i-1)) ) ,
                       Point( bin_w*(i), hist_h - cvRound(g_hist.at<float>(i)) ),
                       Scalar( 0, 255, 0), 2, 8, 0  );
        line( histImage, Point( bin_w*(i-1), hist_h - cvRound(r_hist.at<float>(i-1)) ) ,
                       Point( bin_w*(i), hist_h - cvRound(r_hist.at<float>(i)) ),
                       Scalar( 0, 0, 255), 2, 8, 0  );
    }
    // b_hist.at<float>( i, j ) -> 2D-histogram


    /// Display
    namedWindow("Image", CV_WINDOW_AUTOSIZE );
    imshow("Image", src );
    namedWindow("calcHist", CV_WINDOW_AUTOSIZE );
    imshow("calcHist", histImage );


    waitKey(0);

    return 0;
}
