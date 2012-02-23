parameters = {}


parameters['medianBlur'] = {'ksize':(3,7,lambda x: 2*x+1)}
#Ok


parameters['Canny'] = {'threshold1':(200,600), 'threshold2':(80,600), 'apertureSize': (1,2,lambda x: 2*x + 3)}
# threshold1 find limit...


parameters['erode'] = {'iterations':(1,7), 'kernel':(0,1,lambda x: None)} 

parameters['dilate'] = {'iterations':(1,7), 'kernel':(0,1,lambda x: None)}
