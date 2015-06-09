# -*- coding: utf-8 -*-

# Copyright © 2015, Miguel Madrid Mencía and Daniel Arnao Rodríguez. All rights reserved.
#
# Developed by:
#
# Miguel Madrid Mencía and Daniel Arnao Rodríguez
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# “Software”), to deal with the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimers.
# Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimers in the
# documentation and/or other materials provided with the distribution.
# Neither the names of Miguel Madrid Mencía and Daniel Arnao Rodríguez,
# nor the names of its contributors may be used to endorse or promote
# products derived from this Software without specific prior written
# permission.  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE
# SOFTWARE.

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