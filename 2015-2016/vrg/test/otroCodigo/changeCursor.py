from Tkinter import *

root = Tk()

#
# create a bunch of widgets

Label(root, text="a label").pack()

Button(root, text="a button").pack()

Entry(root, text="an entry").pack()

w = Listbox(root)
for i in range(10):
    w.insert(i, "item %d" % (i+1))
w.pack()

w = Text(root, width=20, height=10)
w.insert(1.0, "a text widget")
w.pack()

#
# second attempt: set a wait cursor on all children
# that doesn't already define their own cursor

class BusyManager:

    def __init__(self, widget):
        self.toplevel = widget.winfo_toplevel()
        self.widgets = {}

    def busy(self, widget=None):

        # attach busy cursor to toplevel, plus all windows
        # that define their own cursor.

        if widget is None:
            w = self.toplevel # myself
        else:
            w = widget

        if not self.widgets.has_key(str(w)):
            try:
                # attach cursor to this widget
                cursor = w.cget("cursor")
                if cursor != "watch":
                    self.widgets[str(w)] = (w, cursor)
                    w.config(cursor="watch")
            except TclError:
                pass

        for w in w.children.values():
            self.busy(w)

    def notbusy(self):
        # restore cursors
        for w, cursor in self.widgets.values():
            try:
                w.config(cursor=cursor)
            except TclError:
                pass
        self.widgets = {}

manager = BusyManager(root)

b = Button(root, text="busy!", command=manager.busy)
b.pack()

b = Button(root, text="not busy!", command=manager.notbusy)
b.pack()

root.mainloop()