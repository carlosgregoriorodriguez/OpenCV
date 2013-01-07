from utils import *
import sys

if __name__ == "__main__":
    debug = False   

    if (len(sys.argv) > 1):
        target = sys.argv[1]
    else:
        target = 0

    camera =  cv2.VideoCapture(target)
        
    func_names = ['Canny']
    
    for name in func_names:
        createTestFrame(name,parameters[name])

    pause = False 
    while 1:
        if not pause:
            img = getFrame(camera,grayscale=True)
        cv2.imshow("original",img)
        for name in func_names:
            test(name,img,eval("cv2."+name),parameters[name])
        pause = InputKey(camera, pause)
