import SimpleCV
import time
display = SimpleCV.Display()
kernel = [[1,2],[-1,2]]
#Imagen del panal
img = SimpleCV.Image("snap.png").convolve(kernel)
#Imagen del panal vacio
img2 = SimpleCV.Image("../images/clean.png").convolve(kernel) 
#Diferencia entre imagenes, en escala de grises
final = (img2 - img).binarize(-1).grayscale().dilate(3).erode(4)
while not display.isDone():
	final.grayscale().show()