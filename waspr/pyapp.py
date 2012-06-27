### PYGAME IN WX ###
#encoding: utf-8
# A simple test of embedding Pygame in a wxPython frame
#
# By David Barker (aka Animatinator), 14/07/2010
 
 
import wx, sys, os, pygame
 
class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()
        if sys.platform == "win32": os.environ['SDL_VIDEODRIVER'] = 'windib'
        os.environ['SDL_WINDOWID'] = str(self.hwnd)
       
        pygame.display.init()
        self.screen = pygame.display.set_mode()
        self.size = self.GetSizeTuple()
       
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
       
        self.fps = 60.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)
 
        self.linespacing = 5
 
    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.Redraw()
 
    def Redraw(self):
        self.screen.fill((0, 0, 0))
 
        cur = 0
 
        while cur <= self.size[1]:
            pygame.draw.aaline(self.screen, (255, 255, 255), (0, self.size[1] - cur), (cur, 0))
           
            cur += self.linespacing
       
        pygame.display.update()
 
    def OnPaint(self, event):
        self.Redraw()
 
    def OnSize(self, event):
        self.size = self.GetSizeTuple()
 
    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source = self.timer)
 
# class Frame(wx.Frame):
#     def __init__(self, parent):
#         wx.Frame.__init__(self, parent, -1)
       
#         #self.display = PygameDisplay(self, -1)
#         panel = wx.Panel(self)

#         # self.statusbar = self.CreateStatusBar()
#         # self.statusbar.SetFieldsCount(3)
#         # # self.statusbar.SetStatusWidths([-3, -4, -2])
#         # self.statusbar.SetStatusText("WaspR", 0)
#         # self.statusbar.SetStatusText("Look, it's a nifty status bar!!!", 1)
       
#         self.Bind(wx.EVT_SIZE, self.OnSize)
#         self.Bind(wx.EVT_CLOSE, self.Kill)
       
#         # # dialog = wx.FileDialog ( None, style = wx.OPEN )
#         # # if dialog.ShowModal() == wx.ID_OK:
#         # #     print 'Selected:', dialog.GetPath()
#         # self.curframe = 0
       
#         vbox = wx.BoxSizer(wx.VERTICAL)
#         hbox1 = wx.BoxSizer(wx.HORIZONTAL)
#         self.SetTitle("WaspR project")
       
#         # self.slider = wx.Slider(self, wx.ID_ANY, 5, 1, 10, style = wx.SL_HORIZONTAL | wx.SL_LABELS)
#         # self.slider.SetTickFreq(0.1, 1)
#         st1 = wx.StaticText(panel, label='Class Name')
#         vbox.Add(st1,flag=wx.RIGHT)
#         self.video = wx.Button(panel, label="Open Video")
#         self.video.Bind(wx.EVT_BUTTON, self.onOpenVideo)
#         vbox.Add(self.video,proportion=1)
#         self.timer = wx.Timer(self)
       
#         self.Bind(wx.EVT_SCROLL, self.OnScroll)
#         self.Bind(wx.EVT_SIZE, self.OnSize)
#         self.Bind(wx.EVT_TIMER, self.Update, self.timer)
       
#         #self.timer.Start((1000.0 / self.display.fps))
       
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         # sizer.Add(self.slider, 0, flag = wx.EXPAND)
#         #sizer.Add(self.display, 1, flag = wx.EXPAND)
       
#         self.SetAutoLayout(True)
#         self.SetSizer(sizer)
#         self.Layout()

#     def onOpenVideo(self, event):
#         """
#         Create and show the Open FileDialog
#         """
#         dlg = wx.FileDialog(
#             self, message="Choose a file",
#             defaultFile="",
#             style=wx.OPEN | wx.CHANGE_DIR
#             )
#         if dlg.ShowModal() == wx.ID_OK:
#             path = dlg.GetPath()
#             print path
#         dlg.Destroy()

#     def Kill(self, event):
#         #self.display.Kill(event)
#         pygame.quit()
#         self.Destroy()
 
#     def OnSize(self, event):
#         self.Layout()
 
#     def Update(self, event):        
#         self.curframe += 1
#         self.statusbar.SetStatusText("Frame %i" % self.display.fps, 2)
 
#     def OnScroll(self, event):
#         return
#         self.display.linespacing = self.slider.GetValue()

class Frame(wx.Frame):
  
    def __init__(self, parent):
        super(Frame, self).__init__(parent, title='WaspR', 
            size=(400, 150))
            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
    
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        fgs = wx.FlexGridSizer(2, 3, 9, 10)

        title = wx.StaticText(panel, label="Video", size=(90, 20))
        author = wx.StaticText(panel, label=u"Panel vacío", size=(90, 20))
        # review = wx.StaticText(panel, label="Review")

        tc1 = wx.TextCtrl(panel)
        tc1_button = wx.Button(panel, label="Explorar...")
        tc2 = wx.TextCtrl(panel)
        tc2_button = wx.Button(panel, label="Explorar...")
        # tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        fgs.AddMany([(title), (tc1, 1, wx.EXPAND), (tc1_button), (author), 
            (tc2, 1, wx.EXPAND), (tc2_button)])

        fgs.AddGrowableCol(1, 1)
        # fgs.AddGrowableRow(1, 1)

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        panel.SetSizer(hbox)
 
class App(wx.App):
    def OnInit(self):
        self.frame = Frame(parent = None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
       
        return True
 
if __name__ == "__main__":
    app = App()
    app.MainLoop()
