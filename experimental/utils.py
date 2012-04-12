from window import Window
from processors.filters import PyrDownProcessor
class DebugWindow (Window):
	show_process = False
	def __init__(self):
		super(DebugWindow,self).__init__(debug=True, processors=[PyrDownProcessor(),PyrDownProcessor()])
