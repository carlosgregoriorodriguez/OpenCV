#-------------------------------------------------
#
# Project created by QtCreator 2013-10-22T12:16:01
#
#-------------------------------------------------

QT       += core

QT       -= gui

TARGET = Differences
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app


SOURCES += main.cpp

INCLUDEPATH += /usr/local/include/opencv

LIBS += -L/usr/local/lib\
-lopencv_core\
-lopencv_imgproc\
-lopencv_highgui\
-lopencv_ml\
-lopencv_video\
-lopencv_features2d\
-lopencv_calib3d\
-lopencv_objdetect\
-lopencv_contrib\
-lopencv_legacy\
-lopencv_flann\
-lopencv_nonfree\
