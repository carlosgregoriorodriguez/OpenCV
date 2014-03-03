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


void mouseHandler(int event, int x, int y, int flags, void* data);


/*
 * 
 */
int main(int argc, char** argv) {
    
    Mat blur, img, img_od, final, eq, img_dst, centers, canny, dst, dst_inv, corner;
    int K = 8;
    int height, width, step, channels;
    //uchar* data;
    Mat img_gray;
    
    
    img = imread("img/img1.jpg");
    
    //ALGORITMO PARA AUMENTAR LAS DIFERENCIAS DE COLORES EN UNA MISMA FOTO Y MEJORAR EL COLOR
    /*cvtColor(img, img, CV_BGR2GRAY);
    //Resize aqui
    
    equalizeHist(img, eq);
    cvtColor(eq, eq, CV_GRAY2BGR);
    */
    //FIN DEL ALGORITMO
    
    //eq por img
    resize(img, img, (Size(612,384)));
    cvtColor(img, img_gray, CV_BGR2GRAY);
    imshow("Original", img);
    //eq por img
    
    
    //ALGORITMO DE DETECCIÓN DE PIEL SANA
    img_od = img.reshape(img.depth(),img.rows*img.cols);
    img_od.convertTo(img_od, CV_32F, 1./255);
    //imshow("IMG_OD", img_od);
    /*
     * Con K = 8 y epsilon 0.5 resultado interesante para las img1 e img2
     * Para la img5 hace falta, de momento, 1.15 de epsilon
     */
    kmeans(img_od,K
            ,img_dst,TermCriteria( CV_TERMCRIT_EPS+CV_TERMCRIT_ITER, 10, 0.5),3, KMEANS_PP_CENTERS, centers);
    //Mat final = img_dst;
    final = img_dst.reshape(img.depth(), img.rows);
    //canny(final, final, threshold1, threshold2);

        //We proceed to invert the "final" image.
    height = final.rows;
    width = final.cols;
    
    //Step es el tamaño de cada fila.
    //step = final.step;
    channels = final.depth();
    
    //Data es un array enorme cuya longitud es height*width
    //data = final.data;

    final.convertTo(final, 16, 255.);
    
    //FIN DEL ALGORITMO
    //imshow("final1", final);
    //waitKey();
    //cout << final.at<int>(5,5);
    threshold(final, dst, 0, 255, THRESH_BINARY);
    threshold(final, dst_inv, 0, 255, THRESH_BINARY_INV);
    
    
    //Invertir la imagen para sacar las cosas malas
    
    
    // AQUI imshow("threshold", dst);
    // AQUI imshow("threshold_inv", dst_inv);
    //GaussianBlur(final, blur, Size(0,0), 4);
    //imshow("GaussianBlur", blur);
    
    //Canny(dst, canny, 1, 1);
    //imshow("Canny", canny);
    
    Mat idea_dst, resultado_idea;
    GaussianBlur(dst_inv,idea_dst,Size(3,3),3);
    fastNlMeansDenoising(idea_dst, idea_dst);
    //threshold(idea_dst, resultado_idea, 0, 255, THRESH_BINARY_INV);
    //Canny(idea_dst, idea_dst, 1, 1);
   // AQUI  imshow("Blur", idea_dst);
    //cornerHarris(dst, corner, 5, 3, 0.04);
    //imshow("Harris", corner);
    Mat output;
    Canny(idea_dst, output, 1, 11);
    vector<vector<Point> > contours;
    vector<Vec4i> hierarchy;
    findContours(output, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0,0));
    
    Mat drawing = Mat::zeros(img_gray.size(), CV_8UC3);
    RNG rng(12345);
    for (vector<vector<Point> >::iterator it = contours.begin(); it!=contours.end(); )
    {
        if (it->size()<90)
            it=contours.erase(it);
        else
            ++it;
    }
    for (int i = 0; i < contours.size(); i++) 
    {
        //Scalar color = Scalar(rng.uniform(0,255));
        drawContours(drawing, contours, i, Scalar(255,255,255), 1, 8, hierarchy, 0, Point());
    }
    
    // AQUI imshow("Resultado_Idea", drawing);
    double alpha, beta;
    alpha = 0.2;
    beta = (1.0 - alpha);
    Mat dst1;
    addWeighted(drawing, alpha, img, beta, 0.0, dst1);
    
    //Create a window
    namedWindow("Contornos", 1);
    //cvSetMouseCallback("Contornos", mouseHandler, &dst1);
    
    imshow("Contornos", dst1);
    
    vector<Mat> channelsEq;
    Mat img_hist_eq;
    
    cvtColor(img,img_hist_eq, CV_BGR2YCrCb);
    split(img_hist_eq, channelsEq);
    equalizeHist(channelsEq[0], channelsEq[0]);
    merge(channelsEq, img_hist_eq);
    cvtColor(img_hist_eq, img_hist_eq, CV_YCrCb2BGR);
    
     namedWindow("EQ", 1);
     
     cvSetMouseCallback("EQ", mouseHandler, &img_hist_eq);
     imshow("EQ", img_hist_eq);
     
     
    
    
    
    

    waitKey();

    //cvtColor(final,final,CV_YUV2BGR);
    //imshow("Resultado", canny);
    //waitKey();
    //cvReleaseImage(&final );
    //delete data;
    return 0;
}


void mouseHandler(int event, int x, int y, int flags, void* data)
{
 
    Mat *img = (cv::Mat*) data;


     if  ( event == EVENT_LBUTTONDOWN )
     {
        cout << "Left button of the mouse is clicked - position (" << x << ", " << y << ")"<< endl;

        int b = img->at<cv::Vec3b>(x,y)[0];
        int g = img->at<cv::Vec3b>(x,y)[1];
        int r = img->at<cv::Vec3b>(x,y)[2];
        cout << "Color (" << r << ", " << g << ", " << b << ")" << endl ;
          
     }
     else if  ( event == EVENT_RBUTTONDOWN )
     {
          cout << "Right button of the mouse is clicked - position (" << x << ", " << y << ")" << endl;
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