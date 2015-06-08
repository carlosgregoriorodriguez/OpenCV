import time

import SimpleCV


if __name__ == '__main__':

    img = SimpleCV.Image("poros papila.bmp")
    inv = img.invert()
    blobs = inv.findBlobs(maxsize=150)
    for blob in blobs:
        # print blob.coordinates()
        # print blob.area()
        blob.draw()
        # img.dl().circle(blob.coordinates(), 10, SimpleCV.Color.GREEN, filled=False)
        # img.dl().circle(blob.coordinates(), 2, SimpleCV.Color.RED, filled=True)

   # blobs.show(color=SimpleCV.Color.GREEN)
    # blobs.draw(color=SimpleCV.Color.GREEN, width=5)
    img.addDrawingLayer(inv.dl())
    img.save("poros papila procesada.bmp")