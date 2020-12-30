from tkinter import Tk, messagebox, filedialog, Text, Menu, Scrollbar, END
from tkinter.messagebox import *
from tkinter.filedialog import *
import os


class Notepad:
    root = Tk()
    
    #root.geometry('600x500')
    Width = 600
    Height = 400
    text_area = Text(root)
    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    edit_menu = Menu(menu_bar, tearoff=0)
    help_menu = Menu(menu_bar, tearoff=0)
    
    scrollbar = Scrollbar(text_area)
    file = None
    
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
        
        # To make the textarea auto resizable 
        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_columnconfigure(0, weight=1)
        
        # Add controls (widget) 
        self.text_area.grid(sticky = 'nsew')
        
        # GUI
        self.menu_bar.add_cascade(labe='File', menu=self.file_menu)
        self.root.config(menu=self.menu_bar)
        # Create new file
        self.file_menu.add_command(label='New', command=self.new_file)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit_app)
            
    def new_file(self):
        self.root.title("Untitled - Notepad")
        self.file = None
        self.text_area.delete(1.0, END)
        
    def open_file(self):
        self.file = askopenfilename(defaultextension=".txt",
            filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')])
        if self.file == "":
            self.file = None
        else:
            self.root.title(os.path.basename(self.file) + " - Notepad")
            self.text_area.delete(1.0, END)
            
            file = open(self.file, 'r')
            self.text_area.insert(1.0, file.read())
            file.close()

    def save_file(self):
        if self.file == None:
            self.file = asksaveasfilename(initialfile='Untitled.txt', 
                defaultextension='.txt', filetypes=[('All Files', '*.*'),
                ('Text Documents', '*.txt')])
            if self.file == "":
                self.file = None
            else:
                file = open(self.file, 'w')
                file.write(self.text_area.get(1.0, END))
                file.close()
                
                self.root.title(os.path.basename(self.file), + " - Notepad")
                
    def quit_app(self):
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()
        
a = Notepad()
a.run()