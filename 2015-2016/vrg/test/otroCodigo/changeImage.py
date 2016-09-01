from Tkinter import *

#----------------------------------------------------------------------

class MainWindow():

    #----------------

    def __init__(self, main):

        # canvas for image
        self.canvas = Canvas(main, width=60, height=60)
        self.canvas.grid(row=0, column=0)

        # images
        self.my_images = []
        self.my_images.append(PhotoImage(file = "ball1.gif"))
        self.my_images.append(PhotoImage(file = "ball2.gif"))
        self.my_images.append(PhotoImage(file = "ball3.gif"))
        self.my_image_number = 0

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW, image = self.my_images[self.my_image_number])

        # button to change image
        self.button = Button(main, text="Change", command=self.onButton)
        self.button.grid(row=1, column=0)

    #----------------

    def onButton(self):

        # next image
        self.my_image_number += 1

        # return to first image
        if self.my_image_number == len(self.my_images):
            self.my_image_number = 0

        # change image
        self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])

#----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()