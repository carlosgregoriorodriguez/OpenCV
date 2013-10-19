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
    String path1= "/home/daniel/git/openCV/2013-2014/Martin-Ismael-Pedro/diferenciasMuestraImagenResta/image1.jpg";
    String path2= "/home/daniel/git/openCV/2013-2014/Martin-Ismael-Pedro/diferenciasMuestraImagenResta/image2.jpg";
    int i;
    cout << "i (para el suavizado):";
    cin >> i;
    calculaDiferencias(path1, path2, i);
    return 0;
}

