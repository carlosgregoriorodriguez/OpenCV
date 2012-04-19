import time, cv2
import numpy as np

class Window(object):
    _window_name = None
    parent = None
    show_process = True
    stop_processor = -1
    def __init__(self, debug=True, processors=[]):
        self.debug = debug
        self.processors = processors
        self.log('Init capture')

    def add_trackbar(self,trackbar):
        trackbar.parent = self if not self.parent else self.parent
        cv2.createTrackbar(trackbar.name,trackbar.window_name,trackbar.default,trackbar.max,trackbar._set_value)

    def log (self,message):
        if self.debug: print '%s: %s'%(self.window_name,message)

    def get_source (self):
        return None

    def _set_window_name (self,name):
        self._window_name = name

    def _get_window_name(self):
        return self._window_name if self._window_name else '%s - %s' % (self.__class__.__name__,id(self))

    window_name = property(_get_window_name,_set_window_name)

    def show(self):
        if self.show_process: 
            cv2.namedWindow(self.processor_window)
            cv2.setMouseCallback(self.processor_window, self.on_mouse_processor)

        cv2.namedWindow(self.window_name)
        for processor in self.processors:
            processor.contribute_to_test(self)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

    def on_mouse(self,*args,**kwargs):
        for processor in self.processors:
            processor.on_mouse(*args,**kwargs)

    def on_key(self,key):
        for processor in self.processors:
            processor.on_key(key)

    def on_mouse_processor(self,event, x, y, flags, param):
        # print event,flags,param
        if flags == cv2.EVENT_FLAG_LBUTTON:
            self.stop_processor = x//(self.all_width//self.all_processors)
            # print self.stop_processor
    def joinImages (self,images):
        # w = images[0].shape[1]
        # h = images[0].shape[0]
        h = 200
        w = int(float(images[0].shape[1])/float(images[0].shape[0])*h)
        # print images[0].shape,w
        resized_imgs = []
        for img in images:
            resized_imgs.append(cv2.resize(img,(w,h)))

        self.all_width =  len(images)*w
        self.all_processors = len(images)

        img = np.zeros((h, self.all_width,3), np.uint8)
        i = 0
        for j in range(len(resized_imgs)):
            if (resized_imgs[j] != None):
                if(len(resized_imgs[j].shape) == 3):
                    img[i*h:(i+1)*h,j*w:(j+1)*w] = resized_imgs[j]
                else:
                    for k in range(3):
                        img[i*h:(i+1)*h,j*w:(j+1)*w,k] = resized_imgs[j]

        return img;

    @property
    def processor_window(self):
        return 'Procesadores %s'%self.window_name

    def paint (self,source):
        img = source
        all_img = [img]
        try:
            before = time.time()
            for processor in self.processors:
                img = processor.process(all_img[-1])
                if img == None: raise Exception('Processor %s doesnt return any image'%processor.__class__.__name__)
                all_img.append(img)
            # img.dtype = np.uint8
            fps = 1/(time.time()-before)

            img = all_img[self.stop_processor]
            if self.debug:
                cv2.putText(img=img, text="%d fps"%fps, org=(20, 20), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                    color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)        
                cv2.putText(img=img, text="%d fps"%fps, org=(20, 20), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, 
                    color=(255, 255, 255), thickness = 1, linetype=cv2.CV_AA)        

            if self.show_process: cv2.imshow(self.processor_window,self.joinImages(all_img))

        except Exception, e:
            # img = cv2.cvtColor(source,cv2.COLOR_GRAY2RGB)
            img = source
            cv2.putText(img=img, text="Error", org=(20, 30), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, 
                    color=(0, 0, 0), thickness = 3, linetype=cv2.CV_AA)        
            cv2.putText(img=img, text="Error", org=(20, 30), 
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.5, 
                    color=(0, 0, 255), thickness = 1, linetype=cv2.CV_AA)        

            self.log('Exception ocurred: %s'%str(e))

        cv2.imshow(self.window_name,img)

