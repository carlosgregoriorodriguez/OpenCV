/* 
 * File:   main.cpp
 * Author: daniel
 *
 * Created on 19 de octubre de 2013, 11:59
 */

#include <cstdlib>
#include "resta.h"
using namespace std;

/*
 * 
 */
int main(int argc, char** argv) {
    String path1= "images/image1.jpg";
    String path2= "images/image2.jpg";

	String path3 = "images/beach1.jpg";
	String path4 = "images/beach2.jpg";


    calculaDiferencias(path3, path4);
    return 0;
}

