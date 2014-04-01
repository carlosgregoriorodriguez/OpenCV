/* 
 * File:   heridas.cpp
 * Author: Daniel
 *
 * Created on 15 de diciembre de 2013, 18:47
 */

#include <cstdlib>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace std;  
using namespace cv;


//Variales globales
const int MAX_CRITERIA = 5;
int K = 8;
int K_MAX = 20;
Mat img;
Mat dst1;
Mat img_od;
Mat img_dst;
Mat final;
Mat dst;
Mat dst_inv;
Mat img_gray;
Mat centers;
Mat img_hist_eq;
void mouseHandler(int event, int x, int y, int flags, void* data);
void colorearArea();
void recortarFoto(int x, int y, Mat image);
void on_trackbar( int, void*) 
{   
    Mat means(K,3, CV_8UC3, Scalar(0));
    if (K==0)K=1;

    kmeans(img_od,K
            ,img_dst,TermCriteria( CV_TERMCRIT_EPS+CV_TERMCRIT_ITER, 10, 0.5),3, KMEANS_PP_CENTERS, centers);

    final = img_dst.reshape(img.depth(), img.rows);
    
    final.convertTo(final, 16, 255.);
    imshow("Salida del kmeans",final);
   // threshold(final, dst, 0, 255, THRESH_BINARY);
   // threshold(final, dst_inv, 0, 255, THRESH_BINARY_INV);
    
    Mat idea_dst, resultado_idea;
   // GaussianBlur(dst_inv,idea_dst,Size(3,3),3);
    //fastNlMeansDenoising(idea_dst, idea_dst);

    Mat output;
    //Canny(idea_dst, output, 1, 11);
    //Canny(idea_dst, output, 80, 100);
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    
    Canny( final, final, 40, 40*2, 3 );
    cv::dilate(final, final, cv::Mat(), cv::Point(-1,-1));
    
    findContours(final, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0,0)); 
    
    

    /// Get the moments
    vector<Moments> mu(contours.size() );
    for( int i = 0; i < contours.size(); i++ )
     { mu[i] = moments( contours[i], false ); }

    ///  Get the mass centers:
    vector<Point2f> mc( contours.size() );
    for( int i = 0; i < contours.size(); i++ )
     { mc[i] = Point2f( mu[i].m10/mu[i].m00 , mu[i].m01/mu[i].m00 ); }
    
    
    
    Mat drawing = Mat::zeros(img_gray.size(), CV_8UC3);
    RNG rng(12345);
    vector<vector<Point> >::iterator it = contours.begin();
    
    vector<Point> approxShape;
    cout << "\t Info: Area and Contour Length \n";
    for (int i = 0; i < contours.size(); i++) 
    {
        //Scalar color = Scalar(rng.uniform(0,255));
        if (it->size() > 20){
            Scalar color = Scalar( rng.uniform(0, 255), rng.uniform(0,255), rng.uniform(0,255) );
            approxPolyDP(contours[i], approxShape, arcLength(Mat(contours[i]), true)*0.04, true);
            drawContours(drawing, contours, i, color, CV_FILLED);   // fill BLUE
            drawContours(drawing, contours, i, Scalar(255, 255, 255), 1, 8, hierarchy, 0, Point());
            ///drawContours(drawing, contours, i, Scalar(255, 255, 255), 2, 8, hierarchy, 0, Point());
            cout << " * Contour[" << i << "] - Area (M_00) = " << mu[i].m00 << " - Area OpenCV: "<< contourArea(contours[i]) <<" - Length: " << arcLength( contours[i], true ) << endl;
            
        }
        it++;
    }
    
    
    //imshow("Resultado_Idea", drawing);
    double alpha, beta;
    alpha = 0.2;
    beta = (1.0 - alpha);
    
    addWeighted(drawing, alpha, img, beta, 0.0, dst1);
    imshow("KMeans", dst1);
    //Create a window
    namedWindow("Contornos", 1);
    //cvSetMouseCallback("Contornos", mouseHandler, &dst1);
    
    imshow("Contornos", dst1);
 
}

Mat aplicaKmeans(string file) {
    //uchar* data;
    img = imread(file);    
    cvtColor(img, img_gray, CV_BGR2GRAY);

    //ALGORITMO DE DETECCIÓN DE PIEL SANA
    img_od = img.reshape(img.depth(),img.rows*img.cols);
    img_od.convertTo(img_od, CV_32F, 1./255);

    namedWindow("KMeans", 1);
    char TrackbarName[50];
    createTrackbar( TrackbarName, "KMeans", &K, K_MAX, on_trackbar);
    on_trackbar(K, 0);
    waitKey(0);
    imwrite("img/resultado.jpg", dst1);
    return dst1;
    
}
void preparaImagen(string file){
    Mat tmp = imread(file);
    resize(tmp, tmp, (Size(750,500)));
    imshow("Original", tmp);
    vector<Mat> channelsEq;
    //Mat img_hist_eq;
    
    cvtColor(tmp,img_hist_eq, CV_BGR2YCrCb);
    split(img_hist_eq, channelsEq);
    equalizeHist(channelsEq[0], channelsEq[0]);
    merge(channelsEq, img_hist_eq);
    cvtColor(img_hist_eq, img_hist_eq, CV_YCrCb2BGR);
    
    namedWindow("EQ", 1);
     
    cvSetMouseCallback("EQ", mouseHandler, &img_hist_eq);
    imshow("EQ", img_hist_eq);
    waitKey(0);
    //imwrite("img/crop.jpg", img_hist_eq);
}

void mouseHandler(int event, int x, int y, int flags, void* data)
{
 
    Mat *img = (cv::Mat*) data;


     if  ( event == EVENT_LBUTTONDOWN )
     {
        cout << "Left button of the mouse is clicked - position (" << x << ", " << y << ")"<< endl;

       
        int bgr [3];
        for (int i = 0; i < 3; i++){
            bgr[i] = 0;  
        }
    
        int margen = 3;
        for (int i = 0; i < 2*margen + 1; i++){
            for (int j = 0; j < 2*margen + 1; j++){
                bgr[0] += img->at<cv::Vec3b>(x + i - margen, y + j - margen)[0];
                bgr[1] += img->at<cv::Vec3b>(x + i - margen, y + j - margen)[1];
                bgr[2] += img->at<cv::Vec3b>(x + i - margen, y + j - margen)[2];
            }
        }
        bgr[0] = bgr[0]/((2*margen + 1)*(2*margen + 1));
        bgr[1] = bgr[1]/((2*margen + 1)*(2*margen + 1));
        bgr[2] = bgr[2]/((2*margen + 1)*(2*margen + 1));
        
        int b = img->at<cv::Vec3b>(x,y)[0];
        int g = img->at<cv::Vec3b>(x,y)[1];
        int r = img->at<cv::Vec3b>(x,y)[2];
        cout << "Color (" << r << ", " << g << ", " << b << ")" << endl ;
        cout << "Color medio (" << bgr[0] << ", " << bgr[1] << ", " << bgr[2] << ")" << endl ;
        //putText(*img, "hoLA", cvPoint(x, y), FONT_HERSHEY_COMPLEX_SMALL, 0.8, Scalar::all(255), 1, 8);
          
     }
     else if  ( event == EVENT_RBUTTONDOWN )
     {
          cout << "Right button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
          
         recortarFoto(x, y, *img);
          
     }
     else if  ( event == EVENT_MBUTTONDOWN )
     {
          cout << "Middle button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
     }
    /* else if ( event == EVENT_MOUSEMOVE )
     {
          cout << "Mouse move over the window - position (" << x << ", " << y << ")" << endl;

     }*/
}


void recortarFoto(int x, int y, Mat image){
    
    Rect roi = Rect(0, y, image.cols, image.rows - y);

    Mat cropped_image = image(roi);
    
    //Create a window
    namedWindow("Recorte", 1);
    
    imshow("Recorte", cropped_image);
    imwrite("img/crop.jpg", cropped_image);
    
}