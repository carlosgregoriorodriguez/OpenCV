from __init__ import *

visualizer = CamSource(
	Window(processors=[
		GrayScaleProcessor(),
		PyrDownProcessor(),
		DFTProcessor(flags=None),
                FormatInt8(),
                ThresholdProcessor(),
		DFTProcessor(flags=DFTProcessor.invs),FormatInt8()
	]),
	DebugWindow()
)
visualizer.show()

#Pretendia que se pudiesen ver las dos ventanas a la vez (con DFT y sin DFT) para poder ver los cambios mejor, pero por lo que veo este metodo no funciona ya que solo mantiene uno de las dos venatanas activas(recibiendo nuevos frames).

#visualizer2 = CamSource(
	#Window(processors=[
		#GrayScaleProcessor(),
		#PyrDownProcessor(),
		##DFTProcessor(flags=None),
                ##FormatInt8(),
                #ThresholdProcessor(),
		##DFTProcessor(flags=DFTProcessor.invs),FormatInt8()
	#]),
	#DebugWindow()
#)
#visualizer2.show()
#visualizer.show()
