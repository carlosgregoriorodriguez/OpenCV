

#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include "buscaobjetos.h"
#include "opencv2/features2d/features2d.hpp"
#include "opencv2/nonfree/features2d.hpp"


using namespace cv;
using namespace std;



//caracteristicas de una imagen con surf

int main(){
   
    Mat img,dst,trozo,featureimg ;
    img = imread( "/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/una.jpg");
    trozo = imread( "/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/dos.jpg" );
    /*img = imread( "/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/scene1.jpg");
    trozo = imread( "/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/waldo.jpg" );*/
    cvtColor(img, img, CV_BGR2GRAY);
    cvtColor(trozo, trozo, CV_BGR2GRAY);
    ///////////PARA UNA FOTO///////////
    // vector of keypoints
    std::vector<cv::KeyPoint> keypoints;
    // señalar puntos de interes aquellos mayores de 20000, en la imagen1
    cv::SurfFeatureDetector surf(1000.); // threshold
    // Detecta las caracteristicas (puntos clave)
    surf.detect(img,keypoints);
    
    ///////////PARA OTRA FOTO///////////
    std::vector<cv::KeyPoint> keypoints1;
    // Señalar como puntos de interes aquellos mayor que 400 en la imagen2
    cv::SurfFeatureDetector surf1(1000.); // threshold
    // Detecta las caracteristicas (puntos clave)
    surf1.detect(trozo,keypoints1);
    
    cv::SurfDescriptorExtractor surfDesc;
    cv::Mat descriptors1;
    //necesitamos el descriptor de puntos para relacionar despues los puntos
    surfDesc.compute(img,keypoints,descriptors1);
    
    cv::SurfDescriptorExtractor surfDesc1;
    cv::Mat descriptors2;
    //necesitamos el descriptor de puntos para relacionar despues los puntos
    surfDesc1.compute(trozo,keypoints1,descriptors2);
    
    
    BFMatcher  matcher(NORM_L2);
    // Match the two image descriptors
    std::vector<cv::DMatch> matches;
    //enlaza los puntos de interes(características)
    //se encarga de relacionar 1 a uno cada caracteristica de cada uno de los descriptores
    matcher.match(descriptors1,descriptors2, matches);
    
    //coge las distancias menores, esto lo hacemos para coger el mismo punto  , el que nos interesa
    std::nth_element(matches.begin(),    // initial position
                     matches.begin()+24, // cogemos solo 24 enlaces
                     matches.end());     // end position
    // remove all elements after the 25th
    matches.erase(matches.begin()+25, matches.end());
    
    cv::Mat imageMatches;
    cv::drawMatches(
                    img,
                    keypoints, // 1st image and its keypoints
                    trozo,
                    keypoints1, // 2nd image and its keypoints
                    matches,            // the matches
                    imageMatches,      // the image produced
                    cv::Scalar(255,255,255)); // color of the lines
    
    namedWindow("resultado");
    imshow("resultado", imageMatches);
    waitKey(0);
    
}
