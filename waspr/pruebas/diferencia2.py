import SimpleCV
import time
display = SimpleCV.Display()
#Imagen del panal
img = SimpleCV.Image("snap.png")
#Imagen del panal vacío
img2 = SimpleCV.Image("../images/clean.png")
#Diferencia entre imágenes, en escala de grises
final = (img2 - img).grayscale()
while not display.isDone():
	final.grayscale().show()