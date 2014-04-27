
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>
#include <math.h>

using namespace std;
using namespace cv;

bool ldown = false; // left mouse button down flag
bool lup = false; // left mouse button up flag

Mat img; // original image

//----Crop
Mat croppedImage; // cropped image
Point corner1, corner2; // Starting and ending of the user's selection point
Rect box; // (ROI)Regions of Interest


// Callback function for mouse events
static void mouse_callback(int event, int x, int y, int, void*) {
    // when left mouse button is pressed
    if (event == EVENT_LBUTTONDOWN) {
        ldown = true;
        // record its position and save it in corner1
        corner1.x = x;
        corner1.y = y;
        cout << "Corner 1 recorded at " << corner1 << endl;
    }
    // when left mouse button is released
    if (event == EVENT_LBUTTONUP) {
        // if user selection is bigger than 20 piexels
        if (abs(x - corner1.x) > 20 && abs(y - corner1.y) > 20) {
            lup = true;
            // record its position and save it in corner1
            corner2.x = x;
            corner2.y = y;
            cout << "Corner 2 recorded at " << corner2 << endl << endl;
        } else {
            cout << "Please select a bigger region" << endl;
            ldown = false;
        }
    }
    // update the box showing the selected region as the user drags the mouse
    if (ldown == true && lup == false) {
        Point pt;
        pt.x = x;
        pt.y = y;
        Mat local_img = img.clone();
        rectangle(local_img, corner1, pt, Scalar(0, 0, 255)); // b, g, r
        imshow("Cropping app", local_img);
    }
    // Define ROI and crop it out when both corners have been selected
    if (ldown == true && lup == true) {
        box.width = abs(corner1.x - corner2.x);
        box.height = abs(corner1.y - corner2.y);
        box.x = min(corner1.x, corner2.x);
        box.y = min(corner1.y, corner2.y);

        // Make a image out of just the selected ROI and display it in a new window
        Mat crop(img, box);
        imshow("Crop", crop);

        // clone the cropped image(ROI) and save it to a file
        croppedImage = img(box).clone();
        imwrite("../Heridas/Foto17-03-14_10_33_21-Recortada.jpg", croppedImage);

        ldown = false;
        lup = false;
    }
}

int main() {
    // Read image
    img = imread("../Heridas/Foto17-03-14_10_33_21.jpg");
    resize(img, img, cv::Size(img.cols / 4, img.rows / 4));
    
    imshow("Cropping app", img);

    setMouseCallback("Cropping app", mouse_callback);

    //Wait spaceBar
    while(cv::waitKey(1) != 32);

    return 0;
}