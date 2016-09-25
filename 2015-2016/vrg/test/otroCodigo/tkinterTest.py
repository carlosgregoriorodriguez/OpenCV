from Tkinter import *
 
root = Tk()
Label(root, text='Click at different\n locations in the frame below').pack()
def callback(event):
	#print dir(event)
	print "you clicked at", event.x, event.y
frame = Frame(root, bg='khaki', width=130, height=80)
frame.bind("<Button-1>", callback)
frame.pack()
root.mainloop()