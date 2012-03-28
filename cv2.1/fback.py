#!/usr/bin/env python

import time
from cv import *

class FBackDemo:
    def __init__(self):
        self.capture = CaptureFromCAM(0)
        #SetCaptureProperty(self.capture, CV_CAP_PROP_POS_FRAMES, 10)
        #does not work, this was a try to reduce the delay.
        self.mv_step = 8
        self.mv_scale = 1.5
        self.mv_color = (0, 255, 0)
        self.mv_color2 = (255,0,0)
        self.cflow = None
        self.flow = None
        self.font1 = InitFont(CV_FONT_HERSHEY_COMPLEX, 1, 1, 0, 1, 8)
        self.original_frame = None

        NamedWindow( "Optical Flow", 1 )

        print( "Press q - quit the program\n" )

    def draw_flow(self, flow, prevgray,time):
        """ Returns a nice representation of a hue histogram """
        k = .5
        CvtColor(prevgray, self.cflow, CV_GRAY2BGR)
        for y in range(0, flow.height, self.mv_step):
            for x in range(0, flow.width, self.mv_step):
                fx, fy = flow[y, x]
                if (abs(fx) > k) and (abs(fy) > k):
                    color = self.mv_color2
                else:
                    color = self.mv_color
                Line(self.cflow, (x,y), (int(x+fx),int(y+fy)), color)
                Circle(self.cflow, (x,y), 1, color, -1)
      
        Resize(self.cflow,self.original_frame)
        PutText (self.original_frame,"time "+str(time)+"s", (10,50), self.font1, (0,0,255));
        ShowImage("Optical Flow", self.original_frame)

    def run(self):
        first_frame = True
        frame = CreateImage((320,240), 8, 3)
        while True:
            self.original_frame = QueryFrame( self.capture )
            while self.original_frame is None:
                print "Lost frame... trying again"
                self.original_frame = QueryFrame (self.capture) 

            Resize(self.original_frame,frame)
            Flip(frame,None,1)
            if first_frame:
                gray = CreateImage(GetSize(frame), 8, 1)
                prev_gray = CreateImage(GetSize(frame), 8, 1)
                flow = CreateImage(GetSize(frame), 32, 2)
                self.cflow = CreateImage(GetSize(frame), 8, 3)
                first_frame = False

            CvtColor(frame, gray, CV_BGR2GRAY)
            if not first_frame:
                t = time.time()                        
                CalcOpticalFlowFarneback(prev_gray, gray, flow,
                    pyr_scale=0.5, levels=3, winsize=15,
                    iterations=2, poly_n=5, poly_sigma=1.1, flags=0)
                self.draw_flow(flow, prev_gray,time.time()-t)
                c = WaitKey(7)
                if c == ord("q"):
                    break
            prev_gray,gray = gray, prev_gray
            

if __name__=="__main__":
    demo = FBackDemo()
    demo.run()
