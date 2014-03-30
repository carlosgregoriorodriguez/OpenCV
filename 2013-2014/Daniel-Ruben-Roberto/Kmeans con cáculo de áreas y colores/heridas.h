/* 
 * File:   heridas.h
 * Author: DanSirak
 *
 * Created on 12 de febrero de 2014, 16:00
 */



#ifndef HERIDAS_H
#define	HERIDAS_H

#include <cstdlib>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"

using namespace std;  
using namespace cv;

Mat aplicaKmeans(string file);
void preparaImagen(string file);

#endif	/* HERIDAS_H */

