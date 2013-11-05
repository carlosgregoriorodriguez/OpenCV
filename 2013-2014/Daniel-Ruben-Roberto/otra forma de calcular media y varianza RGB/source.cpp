#include <opencv2/core/core.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <opencv2/highgui/highgui.hpp>
#include <iostream>
#include <string>

using namespace cv;
using namespace std;




using namespace std;
typedef unsigned char uchar;
int main(int argc, char *argv[])
{

	IplImage *image = cvLoadImage("multimedia/images/botin.jpg", 1);
	CvScalar MeanScalar;
	CvScalar StandardDeviationScalar;
	cvAvgSdv(image, &MeanScalar, &StandardDeviationScalar);

	cout << "Blue Channel Avg is : " << MeanScalar.val[0] << endl;
	cout << "Blue Channel Standard Deviation is: " << StandardDeviationScalar.val[0] << endl;
	cout << "Green Channel Avg is : " << MeanScalar.val[1] << endl;
	cout << "Green Channel Standard Deviation is : " << StandardDeviationScalar.val[1] << endl;
	cout << "Red Channel Avg is : " << MeanScalar.val[2] << endl;
	cout << "Red Channel Standard Deviation is : " << StandardDeviationScalar.val[2] << endl;


	cvNamedWindow("image", 1);
	cvShowImage("image", image);
	cvWaitKey(0);

	return 0;
}