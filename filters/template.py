from utils import *

if __name__ == "__main__":
    debug = False
    camera =  cv2.VideoCapture(0)
        
    func_names = ['erode','dilate','Canny']
    
    for name in func_names:
        createTestFrame(name,parameters[name])
    while 1:
        img = getFrame(camera,grayscale=True)
        cv2.imshow("original",img)
        for name in func_names:
            test(name,img,eval("cv2."+name),parameters[name])
        InputKey(camera)        
