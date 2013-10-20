/* 
 * File:   resta.h
 * Author: daniel
 *
 * Created on 19 de octubre de 2013, 12:50
 */

#ifndef RESTA_H
#define	RESTA_H
#include <iostream>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
using namespace std;
using namespace cv;

cv::Mat cargaImagen(String path);
void calculaDiferencias(String path1, String path2);
void dummy(int, void *);

#endif	/* RESTA_H */

