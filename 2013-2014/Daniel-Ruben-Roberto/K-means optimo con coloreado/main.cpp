#include <cstdlib>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <string>

using namespace std;  
using namespace cv;

void show_result(const cv::Mat& labels, const cv::Mat& centers, int height, int width);
void calcularPorcentajes(Mat image);
int K = 3;


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
        cv::imshow("original", image);
 
        cv::Mat reshaped_image = image.reshape(1, image.cols * image.rows);
        std::cout << "reshaped image: " << reshaped_image.rows << ", " << reshaped_image.cols << std::endl;
        assert(reshaped_image.type() == CV_8UC1);
        //check0(image, reshaped_image);
         
        cv::Mat reshaped_image32f;
        reshaped_image.convertTo(reshaped_image32f, CV_32FC1, 1.0 / 255.0);
        std::cout << "reshaped image 32f: " << reshaped_image32f.rows << ", " << reshaped_image32f.cols << std::endl;
        assert(reshaped_image32f.type() == CV_32FC1);
         
        cv::Mat labels;
        cv::TermCriteria criteria (CV_TERMCRIT_EPS+CV_TERMCRIT_ITER, 100, 1);
        cv::Mat centers;
        cv::kmeans(reshaped_image32f, K, labels, criteria, 1, cv::KMEANS_PP_CENTERS, centers);
 
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
        
        calcularPorcentajes(rgb_image);
        
        cv::imshow("KMedias", rgb_image);
        cv::waitKey();
}

void calcularPorcentajes(Mat image){
    
    int numPixelesColor [K];
    int colores[K][3];
    int numColoresActual = 0;
    
    for (int i = 0; i < K; i++){
        numPixelesColor[i] = 0;  
    }
    
    for (int i = 0; i < image.rows; i++){
        for (int j = 0; j < image.cols; j++){
            bool found = false;
            int n = 0;
            while (!found && (n < K) && (numColoresActual > n)){
                if ((colores[n][0] == image.at<Vec3b>(i,j)[0]) && (colores[n][1] == image.at<Vec3b>(i,j)[1]) && (colores[n][2] == image.at<Vec3b>(i,j)[2]))
                    found = true; 
                else
                    n++;
            }
            if (found)
                numPixelesColor[n]++;
            else{
                if(numColoresActual < K){
                    colores[numColoresActual][0] = image.at<Vec3b>(i,j)[0]; //b
                    colores[numColoresActual][1] = image.at<Vec3b>(i,j)[1]; //g
                    colores[numColoresActual][2] = image.at<Vec3b>(i,j)[2]; //r
                    numPixelesColor[numColoresActual]++;
                    numColoresActual++;
                }
                else{
                    //ERROR! más colores que centros!
                    int b = image.at<Vec3b>(i,j)[0];
                    int g = image.at<Vec3b>(i,j)[1];
                    int r = image.at<Vec3b>(i,j)[2];
                    cout << "EHHH Color de mas . Color (" << r << ", " << g << ", " << b << ")" << endl ;
                    cout << "en la position (" << i << ", " << j << ")" << endl;
          
                }
            }
        }
    }    


    cout << "numColores: " << numColoresActual << endl;
    cout << "numPixeles Totales: " << image.cols*image.rows << endl;
    for (int i = 0; i < K; i++){
        float porcentaje = float(numPixelesColor[i])/float(image.cols*image.rows)*100;
        cout << "color: (" << colores[i][2] << ", " << colores[i][1] << ", "<< colores[i][0] << "). Tiene numPixeles: " << numPixelesColor[i]  
                << ". En porcentaje: " <<  porcentaje << "%" 
                << ". Con suma de las componentes rgb: " << colores[i][2]+colores[i][1]+colores[i][0] << endl;  
    }
    
    cout << "cuanto mayor es la suma de las componentes rgb, menos oscuro es el color, y mas sana esta la piel" << endl;
            
    
    
}