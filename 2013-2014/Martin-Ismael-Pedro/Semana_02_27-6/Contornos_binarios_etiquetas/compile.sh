g++ -ggdb `pkg-config --cflags opencv` -o `basename main .cpp` main.cpp `pkg-config --libs opencv`;
