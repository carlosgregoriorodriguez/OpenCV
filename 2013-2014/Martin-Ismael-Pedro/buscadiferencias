#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;

void dummy(int, void *);
void mouseEvent(int evt, int x, int y, int flags, void* param){
    if(evt==CV_EVENT_LBUTTONDOWN){
        
        Mat image1,image2;
        
        
        image1 = imread("img1.jpg", CV_LOAD_IMAGE_COLOR);
        image2 = imread("img2.jpg", CV_LOAD_IMAGE_COLOR);
        Scalar intensidad = image1.at<uchar>(Point(x, y));
        Scalar intensidad2 = image2.at<uchar>(Point(x, y));
        if (intensidad==intensidad2) {
            printf("Ese punto no es una diferencia \n");
        }
        else{
            printf("BIENN!!!Ese punto SI es una diferencia!!!!! \n" );
        }
        

    }
}

int main( int argc, char** argv )
{
    
    Mat image1,image2;
        image1 = imread("img1.jpg", CV_LOAD_IMAGE_COLOR);
    image2 = imread("img2.jpg",CV_LOAD_IMAGE_COLOR);
    namedWindow("IMAGEN1", CV_WINDOW_AUTOSIZE );//name of window
    
    namedWindow("IMAGEN2", CV_WINDOW_AUTOSIZE );
    imshow("IMAGEN1", image1);//show the window
    cvMoveWindow( "IMAGEN1",  100,100  );
    imshow("IMAGEN2", image2);
    cvMoveWindow( "IMAGEN2", 700, 100 );
    // Check for invalid input
    if(!image1.data || !image2.data )
    {
        cout <<  "Could not open or find the image" << std::endl ;
        return -1;
    }
    printf("pulsa los puntos de la IMAGEN1 para buscar diferencias entre la IMAGEN1 y la IMAGEN2 \n");
    cvSetMouseCallback("IMAGEN1", mouseEvent, 0);
        waitKey(0);
     cvDestroyAllWindows();
}
