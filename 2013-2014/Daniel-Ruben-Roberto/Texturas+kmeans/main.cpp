#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <math.h>
#include <stdio.h>
#include <iostream>

using namespace cv;
using namespace std;

/// Global Variables
int kernel_size = 21;
int pos_sigma = 3; //gaussvar
int pos_lm = 100; //wavelength
int pos_th = 37; //orientation
int pos_psi = 70; //phaseoffset
Mat src_f;
Mat dest;

/// Function Headers
Mat mkKernel(int ks, double sig, double th, double lm, double ps);
void Process(int, void *);
void apply_kmeans(const Mat& image, int cluster_number);
void show_result(const Mat& labels, const Mat& centers, int height, int width);


//4,69,41,75
//3, 27, 49, 76
//3, 100,37,70

/// Function Main

int main(int argc, char** argv) {
    //Mat image = cv::imread("../QUEMADOS/mdcg2695150/20130319/IMG_3981_1500x1000.JPG", 1);
    // Mat image = cv::imread("../QUEMADOS/mpm2673522/27marzo2013/IMG_3997.JPG", 1);
    Mat image = cv::imread("../images/new.jpg", 1);

    resize(image, image, cv::Size(750, 500));
    imshow("Original", image);
    Mat src;
    cvtColor(image, src, CV_BGR2GRAY); //Convert to grey
    src.convertTo(src_f, CV_32F, 1.0 / 255, 0); //Convert to float
    //Kernel size must be pair
    if (!kernel_size % 2) {
        kernel_size += 1;
    }
    namedWindow("Process window", 1);
    createTrackbar("GaussVar(sig)", "Process window", &pos_sigma, kernel_size, Process);
    createTrackbar("Wavelenght(lm)", "Process window", &pos_lm, 100, Process);
    createTrackbar("Orientation(th)", "Process window", &pos_th, 180, Process);
    createTrackbar("PhaseOffset(psi)", "Process window", &pos_psi, 360, Process);
    Process(0, 0); //GaborFilter
    
    waitKey(0);
    
    //Get the last parameters
    int post_sigma = getTrackbarPos("GaussVar(sig)","Process window");
    int post_lm = getTrackbarPos("Wavelenght(lm)","Process window");
    int post_th = getTrackbarPos("Orientation(th)","Process window");
    int post_psi = getTrackbarPos("PhaseOffset(psi)","Process window");

    //Save image
    Mat filtered;
    Mat save;
    Mat saveKernel = mkKernel(kernel_size, post_sigma, post_th, (0.5 + post_lm / 100.0), post_psi);
    filter2D(src_f, filtered, CV_32F, saveKernel); // Apply filter 
    
    //Conver to CV_8UC3
    filtered.convertTo(save, CV_8UC3, 255, 0);
    cvtColor(save,save,CV_GRAY2RGB);
    
    imshow("Gabor", save);
    imwrite("../images/Gabor.jpg", save);

    //K-means
    apply_kmeans(save,3);

    waitKey(0);
    return 0;
}

//Mat getGaborKernel(Size ksize, double sigma, double theta, double lambd, double gamma, double psi=CV_PI*0.5, int ktype=CV_64F )
Mat mkKernel(int ks, double sig, double th, double lm, double ps) {
    int hks = (ks - 1) / 2;
    double theta = th * CV_PI / 180;
    double psi = ps * CV_PI / 180;
    double del = 2.0 / (ks - 1);
    double lmbd = lm;
    double sigma = sig / ks;
    double x_theta;
    double y_theta;
    Mat kernel(ks, ks, CV_32F);
    for (int y = -hks; y <= hks; y++) {
        for (int x = -hks; x <= hks; x++) {
            x_theta = x * del * cos(theta) + y * del * sin(theta);
            y_theta = -x * del * sin(theta) + y * del * cos(theta);
            kernel.at<float>(hks + y, hks + x) = (float) exp(-0.5 * (pow(x_theta, 2) + pow(y_theta, 2)) / pow(sigma, 2)) * cos(2 * CV_PI * x_theta / lmbd + psi);
        }
    }
    return kernel;
}

void Process(int, void *) {
    double sig = pos_sigma;
    double lm = 0.5 + pos_lm / 100.0;
    double th = pos_th;
    double ps = pos_psi;
    ///Gabor Filter
    Mat kernel = mkKernel(kernel_size, sig, th, lm, ps);
    filter2D(src_f, dest, CV_32F, kernel); // Apply filter
    imshow("Process window", dest);
    ///Show kernel image
    Mat Lkernel(kernel_size * 20, kernel_size * 20, CV_32F);
    resize(kernel, Lkernel, Lkernel.size());
    Lkernel /= 2.;
    Lkernel += 0.5;
    imshow("Kernel", Lkernel);
    /// Process window pow 2
    Mat mag;
    pow(dest, 2.0, mag);
    imshow("Process^2", mag);

}

void apply_kmeans(const Mat& image, int cluster_number) {

    assert(image.type() == CV_8UC3);

    Mat reshaped_image = image.reshape(1, image.cols * image.rows);
    assert(reshaped_image.type() == CV_8UC1);

    Mat reshaped_image32f;
    reshaped_image.convertTo(reshaped_image32f, CV_32FC1, 1.0 / 255.0);
    assert(reshaped_image32f.type() == CV_32FC1);

    Mat labels;
    Mat centers;
    kmeans(reshaped_image32f, cluster_number, labels, TermCriteria(CV_TERMCRIT_ITER | CV_TERMCRIT_EPS, 10000, 0.0001), 1, cv::KMEANS_RANDOM_CENTERS, centers);

    show_result(labels, centers, image.rows, image.cols);

}

void show_result(const Mat& labels, const Mat& centers, int height, int width) {
        assert(labels.type() == CV_32SC1);
        assert(centers.type() == CV_32FC1);
         
        Mat imageFinal(height, width, CV_8UC3);
        MatIterator_<Vec3b> img_first = imageFinal.begin<Vec3b>();
        MatIterator_<Vec3b> img_last = imageFinal.end<Vec3b>();
        MatConstIterator_<int> label_first = labels.begin<int>();
         
        Mat centers_u8;
        centers.convertTo(centers_u8, CV_8UC1, 255.0);
        Mat centers_u8c3 = centers_u8.reshape(3);
         
        while ( img_first != img_last ) {
                const Vec3b& cnt = centers_u8c3.ptr<Vec3b>(*label_first)[0];
                *img_first = cnt;
                ++img_first;
                ++label_first;
        }
        imshow("K-means", imageFinal);
        imwrite("../images/GaborK-means.jpg", imageFinal);
        waitKey();
}