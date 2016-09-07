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
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import cvSpace
from astropy.io import fits
import os
import platform

'''MatPlotLib comunication'''
class MatPlotHistogram:
	def __init__(self, master, array=0):
		print "Creating matplotlib canvas"
		self.master=master
		self.setArray(array)
		self.blackLine = -99
		self.difusseLine= -99
		self.peakLine= -99
		self.rtLine = -99
		self.frame = tk.Frame(master)
		self.fig = Figure(figsize=(15, 2.8), dpi=40)
		self.ax = self.fig.add_subplot(111)
		self.iniCanvas()
		
	def setArray(self, array):
		self.array = array
		self.arrayOrig=array
		
	def iniCanvas(self, type = ''):
		self.ax.clear()
		self.ax.set_yscale('log')
		self.ax.set_xlim([0,255])
		self.ax.set_ylim([1,self.array.max(axis=0)])
		
		self.setUpCanvas()
		
		self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
		self.frame.pack()		
	
	def setLine(self, blackLine = -99, difusseLine=-99, peakLine=-99, rtLine=-99):
		print "Poniendo lineas"
		self.ax.clear()
		self.ax.set_yscale('log')
		self.ax.set_xlim([0,255])
		self.ax.set_ylim([1,self.array.max(axis=0)])
		if (blackLine>=0 and blackLine<=255):
			self.blackLine = blackLine
		if (difusseLine>=0 and difusseLine<=255):
			self.difusseLine = difusseLine
		if (peakLine>=0 and peakLine<=255):
			self.peakLine = peakLine
			print "peakLine con valor "+str(peakLine)
		if (rtLine>=0 and rtLine<=255):
			self.rtLine = rtLine
			print "rtLine con valor "+str(peakLine)
		self.p = self.fig.gca()

		self.p.plot(self.array)
		self.plotHistogramFromCalcHistogram()
		self.p.plot([self.blackLine,self.blackLine],[1,self.maxYval], lw=5, color = (0,0,0))
		self.p.plot([self.difusseLine,self.difusseLine],[1,self.maxYval], lw=5, color = (0,1,0))
		self.p.plot([self.peakLine,self.peakLine],[1,self.maxYval], lw=5, color = (0.94,0.92,0.3))
		self.canvas.draw()

	def getLines():
		return self.blackLine, self.difusseLine, self.peakLine
			
	def setUpCanvas(self):
		self.canvas = FigureCanvasTkAgg(self.fig,master=self.master)
		
		self.p = self.fig.gca()

		self.maxYval = self.array.max(axis=0)
		print "[MatPlotHistogram]::iniCanvas Start ###########"
		print "\tsize self.array: "+str(self.array.shape)
		print "\tArray max value: "+str(self.maxYval)
		print "\tArray max value position: "+str(self.array.argmax(axis=0))
		print "[MatPlotHistogram]::iniCanvas  END ############"
		self.p.plot(self.array)
		self.plotHistogramFromCalcHistogram()
		self.p.plot([self.blackLine,self.blackLine],[1,self.maxYval], lw=100, color = (1,0,0))
		self.p.plot([self.difusseLine,self.difusseLine],[1,self.maxYval], lw=100, color = (0,1,0))
		self.p.plot([self.peakLine,self.peakLine],[1,self.maxYval], lw=100, color = (0.94,0.92,0.3))
		self.canvas.show()
	
	def getLines(self):
		return self.blackLine, self.difusseLine, self.peakLine
		
	def plotHistogramFromCalcHistogram(self):
		print "     ----------------------|||||||||||||||||||||||||------------------------"
		print self.array.size
		for n in range(0,int(self.array.size)):
			val = self.array.item(n)
			#print str(n)+" : "+str(val)
			self.p.plot([n,n], [1,val], lw=1, color = (0.6,0.6,0.6))
	
	def getArrayHistogram(self, min = 0, max = 255):
		return self.array[int(min):int(max)]
		
	def getMedianOfSubset(self, min = 0, max =255):
		print "getMedianOfSubset min = "+str(min)+" max = "+str(max)
		tempMedian = cvSpace.getMedianIndex(self.getArrayHistogram(min, max))
		print "GetMedianOfSubset: "+str(tempMedian)
		return int(tempMedian)
		
		
'''AstroImage class stores the astronomical images'''
class AstroImage:
	def __init__(self):
		self.scaleFactor = 1

	def openImage(self, path):
		self.scaleFactor = 1
		self.isFlipped = False
		self.path = path
		splitFilename, splitFileExtension = os.path.splitext(self.path)
		self.name = os.path.basename(self.path)
		print "###########"+self.name
		print "Filename "+splitFilename+" FileExtension "+splitFileExtension
		if (splitFileExtension ==".fits" or splitFileExtension ==".FITS"):
			print "Opening FISTS file"
			self.fitsFile = fits.open(self.path)
			print self.fitsFile.info()
			self.imageCV = cvSpace.preEqualizaFits(self.fitsFile[0].data)
			#self.imageCV = cvSpace.linear(self.fitsFile[0].data)
			#self.imageCV = cvSpace.asinh(self.fitsFile[0].data,0.1)
			self.imageCV = cvSpace.sqrt(self.fitsFile[0].data)
			#self.imageCV = cvSpace.log(self.fitsFile[0].data)
			NaNs = np.isnan(self.imageCV)
			self.imageCV[NaNs] = 0
			inf = np.isinf(self.imageCV)
			self.imageCV[inf] = 0
			#self.imageCV = cvSpace.power(self.fitsFile[0].data, power_index=3)
			#self.imageCV = cvSpace.histeq(self.fitsFile[0].data)
			#self.imageCV = self.fitsFile[0].data
			'''
			self.imageCV = self.imageCV.astype(np.uint8)
			self.imageCV = cv2.equalizeHist(self.imageCV)
			'''
		else:	
			#self.imageCV = cv2.imread(self.path,cv2.IMREAD_GRAYSCALE)
			print "Cargando imagen noReal.jpg"
			self.imageCV = cv2.imread(self.path, cv2.IMREAD_GRAYSCALE)
		print "Image type "+str(type(self.imageCV))
		print "Flux (max, min) = ("+str(self.imageCV.min())+", "+str(self.imageCV.max())+")"
		self.imageCVOriginal = self.imageCV.copy()
		self.thumb = ImageTk.PhotoImage(Image.fromarray(cv2.resize(self.imageCV, (100, 100))))
		self.thumbDark = ImageTk.PhotoImage(Image.fromarray(cv2.resize(self.imageCV, (100, 100))))
		self.thumbDifusse = ImageTk.PhotoImage(Image.fromarray(cv2.resize(self.imageCV, (100, 100))))
		temp8bit = cv2.convertScaleAbs(self.imageCV)
		self.peakThreshold, self.lCandidates, self.peakCVImage = cvSpace.getObjectList(temp8bit)#self.imageCV)
		self.thumbPeak = ImageTk.PhotoImage(Image.fromarray(cv2.resize(self.peakCVImage, (100, 100))))
		self.updateImage()
	
	def statisticalInfo():
		print "Hola"

	def updateImage(self, scaleFactor=1):
		print "[AstroImage::updateImage] self.scaleFactor: "+str(self.scaleFactor)
		self.imagePil = Image.fromarray(self.imageCV)
		self.imageTK = ImageTk.PhotoImage(image=self.imagePil)
		self.histogram = self.updateHistogram()
		
	def invertImage(self):
		self.imageCV = cv2.bitwise_not(self.imageCV)
		self.updateImage(self.scaleFactor)
		
	def	flipImage(self):
		self.isFlipped = True
		self.imageCV = cv2.flip(self.imageCV,0)
		self.updateImage()
		
	def getData(self):
		print self.path
		print self.imageCV.shape
	
	def getImageTK (self):
		return self.imageTK

	def getThumb (self, t):
		if (t=="dark"):
			return self.thumbDark
		elif (t=="difusse"):
			return self.thumbDifusse
		elif (t=="peak"):
			return self.thumbPeak

	
	def modifyThumb(self, thumb="dark", value=-1, value2=-1):
		if (thumb=="DARK"):
			temp = self.imageCVOriginal.copy()
			temp = cv2.resize(temp, (100,100))
			temp = cvSpace.binarice(temp, value)
			temp = Image.fromarray(cv2.resize(temp, (100, 100)))
		elif (thumb=="DIFUSSE"):
			print "Difusse"
			temp = self.imageCVOriginal.copy()
			temp = cv2.resize(temp, (100,100))
			temp = cvSpace.segment(temp, value, value2)
			temp = Image.fromarray(cv2.resize(temp, (100, 100)))
		elif (thumb=="PEAK"):
			print "Peak"
			temp = self.imageCVOriginal.copy()
			temp = cv2.resize(temp, (100,100))
			temp = cv2.bitwise_not(temp)
			temp = cvSpace.binarice(temp, 255-value)
			temp = cv2.bitwise_not(temp)
			temp = Image.fromarray(cv2.resize(temp, (100, 100)))
		return ImageTk.PhotoImage(temp)
		
	def generateDarkImage(self, value=-1):
		temp = self.imageCVOriginal.copy()
		temp = cvSpace.binarice(temp, value)
		return temp
		
	def generateDiffuseImage(self, vMin, vMax):
		print "Binarizando"
		temp = self.imageCVOriginal.copy()
		temp = cvSpace.segment(temp, vMin, vMax)
		return temp
		
	def getImageCV (self):
		return self.imageCV
		temp = cvSpace.binarice(temp, value)
		
	def getImagePil (self):
		return self.imagePil
		
	def scaleUp(self):
		self.height = self.imageTK.height()
		self.width = self.imageTK.width()
		if (self.width<7000 or self.width<7000):
			self.imageTK = ImageTk.PhotoImage(Image.fromarray(cv2.resize(self.imageCV, (self.imageTK.width()*2, self.imageTK.height()*2))))
			self.scaleFactor = self.scaleFactor * 2.0
			print "Scale Up: "+str(self.imageTK.height())

	def scaleDown(self):
		self.height = self.imageTK.height()
		self.width = self.imageTK.width()
		if (self.width>500 or self.width>500):
			self.imageTK = ImageTk.PhotoImage(Image.fromarray(cv2.resize(self.imageCV, (self.imageTK.width()/2, self.imageTK.height()/2))))
			self.scaleFactor = self.scaleFactor / 2.0
			print "Scale Down: "+str(self.imageTK.height())

	def updateHistogram(self):
		print "[AstroImage]Updating histogram"
		#t = cv2.calcHist([self.imageCV], [0], None,[256],[0,256])
		#print t
		return cv2.calcHist([self.imageCV], [0], None,[256],[0,256])
		
	def getHistogram(self):
		return self.histogram
		
'''AstroCanvas class handle the gui and the canvas'''
class AstroCanvas:		
	def __init__(self):
		self.createGui()
		self.canvas = tk.Canvas(self.tabProcessing, width=625, height=400, bg = 'grey', cursor="crosshair")
		self.picker ="MOVE"

	def exit(self):
		root.quit()
		root.destroy()
		
	def createGui(self):
		###main menu
		self.menubar = tk.Menu(root)
		filemenu = tk.Menu(self.menubar, tearoff=0)
		filemenu.add_command(label="Open File", command= self.signalOpenImage)
		filemenu.add_command(label="Save Project", command = self.signalSaveProject)
		filemenu.add_command(label="Save Image")
		filemenu.add_separator()
		filemenu.add_command(label="Options")
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=self.exit)
		self.menubar.add_cascade(label="File", menu=filemenu)

		self.colFreeSpace = tk.BooleanVar()
		self.colDiffuse = tk.BooleanVar()
		self.colPeaks = tk.BooleanVar()
		previewmenu = tk.Menu(self.menubar, tearoff=0)
		previewmenu.add_checkbutton(label="Colorize Free-Space", onvalue=1, offvalue=0, variable=self.colFreeSpace)
		previewmenu.add_checkbutton(label="Colorize Diffuse area", onvalue=1, offvalue=0, variable=self.colDiffuse)
		previewmenu.add_checkbutton(label="Colorize Peaks", onvalue=1, offvalue=0, variable=self.colPeaks)
		previewmenu.add_separator()
		previewmenu.add_command(label="Invert image", command=self.signalInvertImg)
		previewmenu.add_command(label="Flip Image", command=self.signalFlipImg)
		self.menubar.add_cascade(label="Preview", menu=previewmenu)

		helpmenu = tk.Menu(self.menubar, tearoff=0)
		helpmenu.add_command(label="Help Index")
		helpmenu.add_command(label="About...")
		self.menubar.add_cascade(label="Help", menu = helpmenu)
		
		###Zona de manipulacion de la imagen###
		noteFrame = tk.LabelFrame(root, text="Image Manipulation")
		noteFrame.grid(column=0,row=0, padx=5)
		note = notebookExample.Notebook(noteFrame, width= 700, height =680, activefg = 'black', inactivefg = 'grey')  #Create a Note book Instance
		self.tabProcessing = note.add_tab(text = "Proccesing")
		self.tabVector = note.add_tab(text = "Vector")
		self.tabOutput = note.add_tab(text = "Output")
		
		###Set of tools in processing tab###
		toolsFrame = tk.LabelFrame(self.tabProcessing, text="tools")
		toolsFrame.grid(column=0,row=0)

		imgMove = tk.PhotoImage(file="img/move.gif")
		buttonMove = tk.Button(toolsFrame, text = 'Move', image=imgMove, cursor="fleur", command = self.moveCanvas)
		buttonMove.img = imgMove
		buttonMove.grid(column=0, row=0, padx= 10)

		imgScale = tk.PhotoImage(file="img/zoom.gif")
		buttonScaleP = tk.Button(toolsFrame, text = 'zoomIn', image=imgScale, command=self.zoomIn)
		buttonScaleP.img = imgScale
		buttonScaleP.grid( column=0, row=1, padx=10)

		imgScaleL = tk.PhotoImage(file="img/zoomOut.gif")
		buttonScaleL = tk.Button(toolsFrame, text = 'zoomOut', image=imgScaleL, command=self.zoomOut)
		buttonScaleL.img = imgScaleL
		buttonScaleL.grid( column=0, row=2, padx=10)
		separator = tk.Label(toolsFrame, text="  ")
		separator.grid( column=0, row=3, padx=10)
		separator2 = tk.Label(toolsFrame, text="  ")
		separator2.grid( column=0, row=100, padx=10)

		imgDarkPicker = tk.PhotoImage(file="img/darkPicker.gif")
		self.buttonPickDark = tk.Button(toolsFrame, text = 'Move', image=imgDarkPicker, cursor="dotbox", command = self.signalDarkPick)
		self.buttonPickDark.img = imgDarkPicker
		self.buttonPickDark.grid( column=0, row=4, padx=10)
		imgDiffusePicker = tk.PhotoImage(file="img/difussePicker.gif")
		self.buttonPickDiffuse = tk.Button(toolsFrame, text = 'Move', image=imgDiffusePicker, cursor="circle",command = self.signalDifussePick)#state='disabled'
		self.buttonPickDiffuse.img = imgDiffusePicker
		self.buttonPickDiffuse.grid( column=0, row=5, padx=10)
		imgPeackPicker = tk.PhotoImage(file="img/peackPicker.gif")
		self.buttonPickPeack = tk.Button(toolsFrame, text = 'Move', image=imgPeackPicker, cursor="crosshair",command = self.signalStarPick)
		self.buttonPickPeack.img = imgPeackPicker
		self.buttonPickPeack.grid( column=0, row=6, padx=10)	
		
		##GUI right column Info##
		self.infoFrame = tk.LabelFrame(root, text="Main toolbox & info")
		self.infoFrame.grid(column=1,row=0, padx=5)

		self.imgInfoFrame = tk.LabelFrame(self.infoFrame, text="Image Info")
		self.imgInfoFrame.grid(column=1,row=0, padx=5)
		left = tk.Label(self.imgInfoFrame, text="                                                                                  ")
		self.stringVarxCoords = tk.StringVar()
		self.stringVarxCoords.set("X:   --     Y:   --     Flux:   --     \n\n\n\n\n")
		a = tk.Label(self.imgInfoFrame, textvariable=self.stringVarxCoords)
		a.pack()
		left.pack()
		

		self.segmentationFrame = tk.LabelFrame(self.infoFrame, text="Segmentation Information")
		self.segmentationFrame.grid(column=1,row=1, padx=5)
		fluxLabel = tk.Label(self.segmentationFrame, 	text="   Dark Flux Line:")
		fluxLabel.grid(column =0, row=0, padx=10)
		self.fluxDarkIndex = tk.Label(self.segmentationFrame, 	text="--")
		self.fluxDarkIndex.grid(column = 1, row = 0, padx=10)

		difusseLabel = tk.Label(self.segmentationFrame, 	text="   Difusse Flux Line:")
		difusseLabel.grid(column =0, row=1, padx=10)
		self.fluxDifusseIndex = tk.Label(self.segmentationFrame, 	text="--")
		self.fluxDifusseIndex.grid(column = 1, row = 1, padx=10)

		starLabel = tk.Label(self.segmentationFrame, 	text="   Star Flux Line:")
		starLabel.grid(column =0, row=2, padx=10)
		self.fluxPeakIndex = tk.Label(self.segmentationFrame, 	text="--")
		self.fluxPeakIndex.grid(column = 1, row = 2, padx=10)
		
		self.statisticsFrame = tk.LabelFrame(self.infoFrame, text="Image Statistics")
		self.statisticsFrame.grid(column=1,row=2, padx=5)
		left3 = tk.Label(self.statisticsFrame, text=' '*82)
		left3.pack()
		
		self.histEqFrame = tk.LabelFrame(self.infoFrame, text="Histogram equalization")
		self.histEqFrame.grid(column=1,row=3, padx=5)
		left4 = tk.Label(self.histEqFrame, text="                                                                                  ")
		left4.pack()
		
		#Mini canvas Frame
		self.miniCanvasFrame = tk.LabelFrame(self.tabProcessing, text="Segmentation Images")
		self.miniCanvasFrame.grid(column=1,row=3, padx=5, columnspan=5)
		#left = tk.Label(self.miniCanvasFrame, text="       ")
		#left.pack()
		self.miniCanBlack = tk.Canvas(self.miniCanvasFrame, width=100, height=100, bg = 'black', cursor="rtl_logo")
		self.miniCanBlack.grid(column=0,row=0,padx=50)
		self.miniCanDifusse = tk.Canvas(self.miniCanvasFrame, width=100, height=100, bg = 'green', cursor="rtl_logo")
		self.miniCanDifusse.grid(column=1,row=0,padx=50)
		self.miniCanPeak = tk.Canvas(self.miniCanvasFrame, width=100, height=100, bg = 'yellow', cursor="rtl_logo")
		self.miniCanPeak.grid(column=2,row=0,padx=50)
		
	def setCanvas(self, astroIm, update=False):
		#Raster Main image
		self.internalAstroImg = astroIm
		self.imageTK = self.internalAstroImg.getImageTK()
		self.canvasImg = self.canvas.create_image(0,0,  image=self.imageTK)
		self.imgConfigure()

		#Histogram
		self.histogramFrame = tk.LabelFrame(self.tabProcessing, text="Histogram")
		self.histogramFrame.grid(column=1,row=2, padx=5, columnspan=5)

		if (update==False):
			self.matPlotHistogram = MatPlotHistogram(self.histogramFrame, self.internalAstroImg.getHistogram())
			#Raster thumbnails
			self.thumbDarkAstro = self.internalAstroImg.getThumb("dark")
			self.thumbDarkImage = self.miniCanBlack.create_image(50,50,  image=self.thumbDarkAstro)

			self.thumbDifusseAstro = self.internalAstroImg.getThumb("difusse")
			self.thumbDifusseImage = self.miniCanDifusse.create_image(50,50,  image=self.thumbDifusseAstro)

			self.thumbPeakAstro = self.internalAstroImg.getThumb("peak")
			self.thumbPeakImage = self.miniCanPeak.create_image(50,50,  image=self.thumbPeakAstro)

			#Calculate background:
			blackMedian, nIter = cvSpace.sky_median_sig_clip(self.internalAstroImg.imageCVOriginal, 5, 0.1, max_iter=20)
			self.fluxDarkIndex.config(text = str(blackMedian))
			self.fluxPeakIndex.config(text = str(int(self.internalAstroImg.peakThreshold)))
			print "blackMedian: "+str(blackMedian)+" nIter: "+str(nIter)
			self.thumbDarkAstro = self.internalAstroImg.modifyThumb(thumb= "DARK", value = blackMedian)
			self.miniCanBlack.itemconfigure(self.thumbDarkImage, image=self.thumbDarkAstro)
			#Draw line on histogram
			self.matPlotHistogram.setLine(blackLine = int(blackMedian))
			#TODO: change for the median of the subHistogram from blackMedian to self.internalAstroImg.peakThreshold
			tempDiffuseLine = int(blackMedian+self.internalAstroImg.peakThreshold/2)
			if (tempDiffuseLine>self.internalAstroImg.peakThreshold*0.9):
				tempDiffuseLine = tempDiffuseLine * 0.85
			tempDiffuseLine = self.matPlotHistogram.getMedianOfSubset(blackMedian, self.internalAstroImg.peakThreshold)
			self.matPlotHistogram.setLine(difusseLine = tempDiffuseLine)
			self.fluxDifusseIndex.config(text = str(tempDiffuseLine))
			self.matPlotHistogram.setLine(peakLine = int(self.internalAstroImg.peakThreshold))
			#Calculate halo or diffuse image:
			
		#self.internalHistogram.setLine(blackLine = blackMedian)
	def getMainImageCoords(self):
		print self.canvas.coords(self.canvasImg)	
	
	def setHistogram(self, histogram):
		self.internalHistogram = histogram
	
	def imgConfigure(self):
		self.canvas.coords(self.canvasImg,self.imageTK.width()/2,self.imageTK.height()/2)
		self.canvas.itemconfigure(self.canvasImg, image=self.imageTK)
		self.canvas.grid(column=1, row=0)
		self.canvas.bind("<Motion>", self.imageCoordsFlux)
	
	def scroll_start(self, event):
		self.canvas.scan_mark(event.x, event.y)

	def scroll_move(self, event):
		self.canvas.scan_dragto(event.x, event.y, gain=1)
		
	def moveCanvas(self):
		print "Move picker: "+self.picker
		print (self.getMainImageCoords())
		self.canvas.bind("<ButtonPress-1>", self.scroll_start)
		self.canvas.bind("<B1-Motion>", self.scroll_move)
		self.canvas.configure(cursor="fleur")
			
	def zoomIn(self):
		self.internalAstroImg.scaleUp()
		self.setCanvas(self.internalAstroImg, update=True)

	def zoomOut(self):
		self.internalAstroImg.scaleDown()
		self.setCanvas(self.internalAstroImg, update=True)
	
	def signalOpenImage(self):
		self.filePath = tkFileDialog.askopenfilename(filetypes=[("All","*.*"),("Jpg","*.jpg"),("PNG","*.png"), ("GIF","*.gif"),("Fits","*.fits")])
		self.internalAstroImg.openImage(self.filePath)
		self.setCanvas(self.internalAstroImg)
		#self.buttonPickDiffuse.config(state="disabled")
		print self.filePath
		
	def signalInvertImg(self):
		self.internalAstroImg.invertImage()
		self.setCanvas(self.internalAstroImg, update=True)

	def signalFlipImg(self):
		self.internalAstroImg.flipImage()
		self.setCanvas(self.internalAstroImg, update=True)
		
	def signalDarkPick(self):
		#print "Pick Dark Flux"
		self.picker = "DARK"
		self.canvas.configure(cursor="dotbox")
		self.canvas.bind("<ButtonPress-1>", self.signalLine) 

	def signalDifussePick(self):
		#print "Pick Difusse Flux"
		self.picker = "DIFUSSE"
		self.canvas.configure(cursor="circle")
		self.canvas.bind("<ButtonPress-1>", self.signalLine) 

	def signalStarPick(self):
		#print "Pick Star Flux"
		self.picker = "PEAK"
		self.canvas.configure(cursor="crosshair")
		self.canvas.bind("<ButtonPress-1>", self.signalLine) 
			
	def imageCoordsFlux(self, event):
		x, y = self.canvas.canvasx(event.x)/self.internalAstroImg.scaleFactor, self.canvas.canvasy(event.y)/self.internalAstroImg.scaleFactor
		ySource, xSource = self.internalAstroImg.imageCVOriginal.shape
		scaleText = "Image Scale: "+str(self.internalAstroImg.scaleFactor)+"  ("+str(int(x*self.internalAstroImg.scaleFactor))+", "+str(int(y*self.internalAstroImg.scaleFactor))+")\n"
		if ((x<0 or y<0) or (x>=xSource or y>=ySource)):
			text = "X:%(xCoord) 2s    Y:%(yCoord) 2s    Flux:%(f) 2s"%{"xCoord":"--","yCoord":"--","f":"--"}
		else:
			flux = self.internalAstroImg.imageCVOriginal[int(y),int(x)]
			if np.isinf(flux):
				flux = 0
			text = "X:%(xCoord) 2d    Y:%(yCoord) 2d    Flux:%(f) 2d"%{"xCoord":int(x),"yCoord":int(y),"f":float(flux)}
		text = text+"\n__________________________________________\n"+"Image Size:              "+str(xSource)+" x "+str(ySource)+"\nImage Scale Factor:                "+str(self.internalAstroImg.scaleFactor)+"\n"
		self.stringVarxCoords.set(text+scaleText+"ImageName: "+self.internalAstroImg.name)
		#self.matPlotHistogram.setLine(rtLine = flux)
		
	def signalLine(self, event):
		#TODO: considerar caso image flipped self.isFlipped = True
		x, y = self.canvas.canvasx(event.x)/self.internalAstroImg.scaleFactor, self.canvas.canvasy(event.y)/self.internalAstroImg.scaleFactor
		pickedFlux = int(self.internalAstroImg.imageCVOriginal[int(y),int(x)])
		blackLine, difusseLine, peakLine = self.matPlotHistogram.getLines()

		if (self.picker == "DARK"):
			self.matPlotHistogram.setLine(blackLine=pickedFlux)
			self.buttonPickDiffuse.config(state="normal")
			#self.blackLine self.difusseLine self.rtLine
			self.canvas.config(cursor="wait")
			self.thumbDarkAstro = self.internalAstroImg.modifyThumb(thumb= "DARK", value = pickedFlux)
			self.miniCanBlack.itemconfigure(self.thumbDarkImage, image=self.thumbDarkAstro)
			self.canvas.config(cursor="dotbox")
			self.fluxDarkIndex.config(text = str(pickedFlux))

		if (self.picker == "DIFUSSE"):
			self.matPlotHistogram.setLine(difusseLine=pickedFlux)
			self.canvas.config(cursor="wait")
			self.thumbDifusseAstro = self.internalAstroImg.modifyThumb(thumb= "DIFUSSE", value = blackLine, value2=pickedFlux)
			self.miniCanDifusse.itemconfigure(self.thumbDifusseImage, image=self.thumbDifusseAstro)
			self.canvas.config(cursor="circle")
			self.fluxDifusseIndex.config(text = str(pickedFlux))
			
		if (self.picker == "PEAK"):
			self.matPlotHistogram.setLine(peakLine=pickedFlux)
			self.canvas.config(cursor="wait")
			self.thumbPeakAstro = self.internalAstroImg.modifyThumb(thumb= "PEAK", value = int(pickedFlux*.75))
			self.miniCanPeak.itemconfigure(self.thumbPeakImage, image=self.thumbPeakAstro)
			self.canvas.config(cursor="crosshair")
			self.fluxPeakIndex.config(text = str(pickedFlux))
	
	def signalSaveProject(self):
		#todo: open modal dialog window to ask project name....
		print "Saving project"
		#Equalized image
		cv2.imwrite('output/cvMainImage.png',self.internalAstroImg.imageCV)
		#Dark image
		print self.matPlotHistogram.getLines()[0]
		#dark = cvSpace.erode(self.internalAstroImg.generateDarkImage(self.matPlotHistogram.getLines()[0]))
		dark = self.internalAstroImg.generateDarkImage(self.matPlotHistogram.getLines()[0])
		cv2.imwrite('output/cvDarkImage.png',dark)
		#halo or difusse image
		diffuse = self.internalAstroImg.generateDiffuseImage(self.matPlotHistogram.getLines()[0],100)
		cv2.imwrite('output/CUTcvDiffuseImage.png',diffuse)
		diffuseEroded = cvSpace.dilate(diffuse,2)
		diffuseEroded = cvSpace.erode(diffuseEroded,10)
		cv2.imwrite('output/cvDiffuseImage.png',diffuseEroded)
		#save 4 images
		#save file with histogram dark, diffuse and peak lines. In this file, store star and galaxies with categorization.
		
if __name__ == "__main__":		
	root = tk.Tk()
	root.resizable(width=False, height=False)
	root.geometry('1000x735')
	root.title("Simple Space Object Cataloger")

	astroImage = AstroImage()
	astroImage.openImage("test.png")

	astroCanvas = AstroCanvas()
	astroCanvas.setCanvas(astroImage)
	
	if (platform.system()=='Windows'):
		root.iconbitmap('img/appIcon.ico')
	root.config(menu=astroCanvas.menubar)

	root.mainloop()