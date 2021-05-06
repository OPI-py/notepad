import tkinter as tk


class LineEnumerator(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            line_num = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=line_num)
            i = self.textwidget.index("%s+1line" % i)