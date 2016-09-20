import numpy as np
import cv2
import Tkinter as tk
import notebookExample
import PIL
from PIL import ImageTk
from PIL import Image
import sys
import tkFileDialog
import platform

root = tk.Tk()

def createMenu():
	menubar = tk.Menu(root)
	###MENU SUPERIOR###
	filemenu = tk.Menu(menubar, tearoff=0)
	filemenu.add_command(label="Open File", command= openImage)
	filemenu.add_command(label="Save Project")
	filemenu.add_command(label="Save Image")
	filemenu.add_separator()
	filemenu.add_command(label="Options")
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	colFreeSpace = tk.BooleanVar()
	colDiffuse = tk.BooleanVar()
	colPeaks = tk.BooleanVar()
	previewmenu = tk.Menu(menubar, tearoff=0)
	previewmenu.add_checkbutton(label="Colorize Free-Space", onvalue=1, offvalue=0, variable=colFreeSpace)
	previewmenu.add_checkbutton(label="Colorize Diffuse area", onvalue=1, offvalue=0, variable=colDiffuse)
	previewmenu.add_checkbutton(label="Colorize Peaks", onvalue=1, offvalue=0, variable=colPeaks)
	previewmenu.add_separator()
	previewmenu.add_command(label="Invert image")
	previewmenu.add_command(label="Flip Image")
	menubar.add_cascade(label="Preview", menu=previewmenu)

	helpmenu = tk.Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Help Index")
	helpmenu.add_command(label="About...")
	menubar.add_cascade(label="Help", menu = helpmenu)
	return menubar
	
def openImage():
	filePath = tkFileDialog.askopenfilename(filetypes=[("All","*.*"),("Jpg","*.jpg"),("PNG","*.png"), ("GIF","*.gif"),("Fits","*.fits")])
	print filePath
	return filePath
	'''
	img = cv2.imread(filePath,0)
	im = Image.fromarray(img)
	imgtk = ImageTk.PhotoImage(image=im)
	canvasImgComfigure(canvasImg,imgtk)
	scaleFactor =1
	return filePath
	'''

'''	
def createManipulationIm():
	###Zona de manipulacion de la imagen###
	noteFrame = tk.LabelFrame(root, text="Image Manipulation")
	noteFrame.grid(column=0,row=0, padx=5)
	note = notebookExample.Notebook(noteFrame, width= 700, height =680, activefg = 'black', inactivefg = 'grey')  #Create a Note book Instance
	tabProcessing = note.add_tab(text = "Proccesing")
	tabVector = note.add_tab(text = "Vector")
	tabOutput = note.add_tab(text = "Output")
	
	###Conjunto de herramientas###

	toolsFrame = tk.LabelFrame(tabProcessing, text="tools")
	toolsFrame.grid(column=0,row=0)

	imgMove = tk.PhotoImage(file="img/move.gif")
	buttonMove = tk.Button(toolsFrame, text = 'Move', image=imgMove, cursor="fleur")
	buttonMove.img = imgMove
	buttonMove.grid(column=0, row=0, padx= 10)

	imgScale = tk.PhotoImage(file="img/zoom.gif")
	buttonScaleP = tk.Button(toolsFrame, text = 'zoomIn', image=imgScale)#, command=zoomIn)
	buttonScaleP.img = imgScale
	buttonScaleP.grid( column=0, row=1, padx=10)

	imgScaleL = tk.PhotoImage(file="img/zoomOut.gif")
	buttonScaleL = tk.Button(toolsFrame, text = 'zoomOut', image=imgScaleL)#, command=zoomOut)
	buttonScaleL.img = imgScaleL
	buttonScaleL.grid( column=0, row=2, padx=10)
	separator = tk.Label(toolsFrame, text="  ")
	separator.grid( column=0, row=3, padx=10)
	separator2 = tk.Label(toolsFrame, text="  ")
	separator2.grid( column=0, row=100, padx=10)

	imgDarkPicker = tk.PhotoImage(file="img/darkPicker.gif")
	buttonPickDark = tk.Button(toolsFrame, text = 'Move', image=imgDarkPicker)
	buttonPickDark.img = imgDarkPicker
	buttonPickDark.grid( column=0, row=4, padx=10)
	imgDiffusePicker = tk.PhotoImage(file="img/difussePicker.gif")
	buttonPickDiffuse = tk.Button(toolsFrame, text = 'Move', image=imgDiffusePicker)
	buttonPickDiffuse.img = imgDiffusePicker
	buttonPickDiffuse.grid( column=0, row=5, padx=10)
	imgPeackPicker = tk.PhotoImage(file="img/peackPicker.gif")
	buttonPickPeack = tk.Button(toolsFrame, text = 'Move', image=imgPeackPicker)
	buttonPickPeack.img = imgPeackPicker
	buttonPickPeack.grid( column=0, row=6, padx=10)

	return tabProcessing
'''