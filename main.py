from tkinter import (Tk, messagebox, filedialog, Text, Menu, Scrollbar, END,
    INSERT, ttk, Canvas, IntVar, Label)
from tkinter.messagebox import *
from tkinter.filedialog import *
import os

class Notepad:
    root = Tk()
    Width = 700
    Height = 550
    
    text_area = Text(root, undo=True)
    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    edit_menu = Menu(menu_bar, tearoff=0)
    theme_edit = Menu(edit_menu, tearoff=0)
    help_menu = Menu(menu_bar, tearoff=0)
    popup_menu = Menu(root, tearoff=0)
    
    scrollbar = Scrollbar(text_area)
    file = None
    
    variable_marker = IntVar()
    
    canvas = Canvas(text_area, width=1, height=Height,
            highlightthickness=0, bg='lightgrey')
            
    statusbar = Label(root, text="Characters: 0", relief=FLAT, anchor=E)
    
    def __init__(self):
        self.root.title("Untitled - Notepad")
  
        # Center the window
        screen_width = self.root.winfo_screenwidth() 
        screen_height = self.root.winfo_screenheight() 
        # For left-alling
        left = (screen_width / 2) - (self.Width / 2)  
        # For right-allign
        top = (screen_height / 2) - (self.Height /2)  
        # For top and bottom
        self.root.geometry('%dx%d+%d+%d' % (self.Width, self.Height,
            left, top))
        # Make the textarea auto resizable
        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_columnconfigure(0, weight=1)
        # Make textarea size as window
        self.text_area.grid(sticky = 'nsew')
        
        ## GUI
        self.root.config(menu=self.menu_bar)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        # File menu
        self.file_menu.add_command(label='New', accelerator='Ctrl+N', 
            command=self.new_file)
        self.file_menu.add_command(label='Open', accelerator='Ctrl+O',
            command=self.open_file)
        self.file_menu.add_command(label='Save', accelerator='Ctrl+S',
            command=self.save_file)
        self.file_menu.add_command(label='Save as ...',
            accelerator='Ctrl+Alt+S', command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit_app)
        # Edit menu
        self.edit_menu.add_command(label="Copy", accelerator='Ctrl+C',
            command=self.copy)
        self.edit_menu.add_command(label="Paste", accelerator='Ctrl+V',
            command=self.paste)
        self.edit_menu.add_command(label="Select all", accelerator='Ctrl+A',
            command=self.select_all)
        self.edit_menu.add_checkbutton(label='Vertical marker',
            onvalue=1, offvalue=0, variable=self.variable_marker,
            command=self.vertical_line)
        #Nested Theme menu
        self.edit_menu.add_cascade(label='Color theme', menu=self.theme_edit)
        self.theme_edit.add_command(label="Black", command=self.black_theme)
        self.theme_edit.add_command(label="White", command=self.white_theme)
        # Help menu
        self.help_menu.add_command(label="About", command=self.about)
        
        # Mouse right click popup menu
        self.popup_menu.add_command(label="Copy", accelerator='Ctrl+C',
            command=self.copy)
        self.popup_menu.add_command(label="Paste", accelerator='Ctrl+V',
            command=self.paste)
        self.popup_menu.add_command(label="Cut", accelerator='Ctrl+X',
            command=self.cut)
        self.popup_menu.add_command(label="Undo", accelerator='Ctrl+Z',
            command=self.undo)
        self.popup_menu.add_command(label="Redo", accelerator='Ctrl+R',
            command=self.redo)
        # Button bind
        self.text_area.bind('<<Modified>>', self.text_area_modified)
        self.text_area.bind('<ButtonRelease-3>', self.popup)
        self.text_area.bind('<Control-r>', self.redo)
        self.text_area.bind('<Control-z>', self.undo)
        self.text_area.bind('<Control-a>', self.select_all)
        self.text_area.bind('<Control-s>', self.save_file)
        self.text_area.bind('<Control-Alt-s>', self.save_file_as)
        self.text_area.bind('<Control-n>', self.new_file)
        self.text_area.bind('<Control-o>', self.open_file)
        
        # Configure scrollbar
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.text_area.yview,
            cursor="sb_v_double_arrow")
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        
        self.text_area.bind('<Tab>', self.tab)
        # Statusbar
        self.statusbar.grid(sticky='wes')
        
    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
    
    def new_file(self, event=None):
        self.root.title("Untitled - Notepad")
        self.file = None
        self.text_area.delete(0.0, END)
        
    def open_file(self, event=None):
        self.file = askopenfilename(defaultextension=".txt",
            filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')])
        if self.file == "":
            self.file = None
        else:
            self.root.title(os.path.basename(self.file) + " - Notepad")
            self.text_area.delete(0.0, END)
            file = open(self.file, 'r')
            self.text_area.insert(0.0, file.read())
            file.close()

    def save_file_as(self, event=None):
        asksaveasfilename(initialfile='Untitled.txt', 
            defaultextension='.txt', filetypes=[('All Files', '*.*'),
            ('Text Documents', '*.txt')])
            
    def save_file(self, event=None):
        if self.file is not None and self.file != "":
            with open(self.file, 'w') as file:
                    file.write(self.text_area.get(1.0, END))
            self.root.title(os.path.basename(self.file))
        else:
            self.save_file_as()
                            
    def quit_app(self):
        self.root.destroy()
    
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
        
    def cut(self, event=None):
        self.text_area.event_generate("<<Cut>>")
        
    def paste(self):
        self.text_area.event_generate("<<Paste>>")
        
    def undo(self, event=None):
        self.text_area.event_generate("<<Undo>>")
        
    def redo(self, event=None):
        self.text_area.event_generate("<<Redo>>")
        
    def select_all(self, event=None):
        self.text_area.event_generate("<<SelectAll>>")
    
    def about(self):
        showinfo("Notepad", "Simple but Good :)")
    
    def run(self):
        self.root.mainloop()
        
    def tab(self, arg):
        self.text_area.insert(INSERT, " " * 4)
        return 'break'

    def black_theme(self):
        self.text_area.config(bg='black', fg='white',
            insertbackground='white')
    
    def white_theme(self):
        self.text_area.config(bg='white', fg='black',
            insertbackground='black')
       
    def vertical_line(self):
        if self.variable_marker.get() == 1:
            self.canvas.place(x=640)
        elif self.variable_marker.get() == 0:
            self.canvas.place_forget()  # Unmap widget
        else:
            return "Error"
            
    def text_area_modified(self, event=None):
        if self.text_area.edit_modified():
            self.statusbar.config(text="Characters: " + 
                str(len(self.text_area.get(1.0, 'end-1c'))))
        self.text_area.edit_modified(False)

a = Notepad()
a.run()
