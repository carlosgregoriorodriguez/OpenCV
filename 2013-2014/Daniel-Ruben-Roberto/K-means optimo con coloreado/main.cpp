#include <cstdlib>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"


using namespace std;  
using namespace cv;

void show_result(const cv::Mat& labels, const cv::Mat& centers, int height, int width);

/*
 * 
 */
int main(int argc, char** argv) {
    
    cv::Mat image = cv::imread("img/crop.jpg");
        if ( image.empty() ) {
                std::cout << "unable to load an input image\n";
                return 1;
        }
         
        std::cout << "image: " << image.rows << ", " << image.cols << std::endl;
        assert(image.type() == CV_8UC3);
        cv::imshow("image", image);
 
        cv::Mat reshaped_image = image.reshape(1, image.cols * image.rows);
        std::cout << "reshaped image: " << reshaped_image.rows << ", " << reshaped_image.cols << std::endl;
        assert(reshaped_image.type() == CV_8UC1);
        //check0(image, reshaped_image);
         
        cv::Mat reshaped_image32f;
        reshaped_image.convertTo(reshaped_image32f, CV_32FC1, 1.0 / 255.0);
        std::cout << "reshaped image 32f: " << reshaped_image32f.rows << ", " << reshaped_image32f.cols << std::endl;
        assert(reshaped_image32f.type() == CV_32FC1);
         
        cv::Mat labels;
        int cluster_number = 3;
        cv::TermCriteria criteria (CV_TERMCRIT_EPS+CV_TERMCRIT_ITER, 100, 1);
        cv::Mat centers;
        cv::kmeans(reshaped_image32f, cluster_number, labels, criteria, 1, cv::KMEANS_PP_CENTERS, centers);
 
        show_result(labels, centers, image.rows, image.cols);
}



void show_result(const cv::Mat& labels, const cv::Mat& centers, int height, int width)
{
        std::cout << "===\n";
        std::cout << "labels: " << labels.rows << " " << labels.cols << std::endl;
        std::cout << "centers: " << centers.rows << " " << centers.cols << std::endl;
        assert(labels.type() == CV_32SC1);
        assert(centers.type() == CV_32FC1);
         
        cv::Mat rgb_image(height, width, CV_8UC3);
        cv::MatIterator_<cv::Vec3b> rgb_first = rgb_image.begin<cv::Vec3b>();
        cv::MatIterator_<cv::Vec3b> rgb_last = rgb_image.end<cv::Vec3b>();
        cv::MatConstIterator_<int> label_first = labels.begin<int>();
         
        cv::Mat centers_u8;
        centers.convertTo(centers_u8, CV_8UC1, 255.0);
        cv::Mat centers_u8c3 = centers_u8.reshape(3);
         
        while ( rgb_first != rgb_last ) {
                const cv::Vec3b& rgb = centers_u8c3.ptr<cv::Vec3b>(*label_first)[0];
                *rgb_first = rgb;
                ++rgb_first;
                ++label_first;
        }
        cv::imshow("KMedias", rgb_image);
        cv::waitKey();
}