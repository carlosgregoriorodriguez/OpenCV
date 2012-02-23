parameters = {}
parameters['blur'] = {'ksize':(3,7,lambda x: 2*x+1)}
parameters['Canny'] = {'threshold1':(200,600), 'threshold2':(80,600), 'apertureSize': (1,2,lambda x: 2*x + 3)}
