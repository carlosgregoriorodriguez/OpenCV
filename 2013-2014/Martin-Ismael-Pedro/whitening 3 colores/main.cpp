/*#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <opencv2/opencv.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <stdio.h>*/

#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>
#include "whitening.h"

using namespace cv;
using namespace std;


int main(){
    Mat src,dst,dst1,dst2 ;
    src=imread("/Users/pedrete_142/Documents/proyectoprimeroopencv/multimedia/images/beach1.jpg" );
    
    Whitening wh(src);

    wh.whitening();
   
    waitKey(0);
    
}
