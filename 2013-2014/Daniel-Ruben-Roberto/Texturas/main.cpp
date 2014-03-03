#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <math.h>

using namespace cv;
using namespace std;

/// Global Variables
int kernel_size = 21;
int pos_sigma = 5;      //gaussvar
int pos_lm = 50;        //wavelength
int pos_th = 0;         //orientation
int pos_psi = 90;       //phaseoffset
Mat src_f;
Mat dest;

/// Function Headers
Mat mkKernel(int ks, double sig, double th, double lm, double ps);
void Process(int, void *);

//4,69,41,75
//3, 27, 49, 76

/// Function Main
int main(int argc, char** argv) {
    //Mat image = cv::imread("../QUEMADOS/mdcg2695150/20130319/IMG_3981_1500x1000.JPG", 1);
    Mat image = cv::imread("../QUEMADOS/mpm2673522/27marzo2013/IMG_3997.JPG", 1);
    
    resize(image, image, cv::Size(750, 500));
    imshow("Original", image);
    Mat src;
    cvtColor(image, src, CV_BGR2GRAY); //Convert to grey
    src.convertTo(src_f, CV_32F, 1.0 / 255, 0); //Convert to float
    //Kernel size must be pair
    if (!kernel_size % 2) {
        kernel_size += 1;
    }
    namedWindow("Process window",1);
    createTrackbar("GaussVar(sig)", "Process window", &pos_sigma, kernel_size, Process);
    createTrackbar("Wavelenght(lm)", "Process window", &pos_lm, 100, Process);
    createTrackbar("Orientation(th)", "Process window", &pos_th, 180, Process);
    createTrackbar("PhaseOffset(psi)", "Process window", &pos_psi, 360, Process);
    Process(0, 0); //GaborFilter
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