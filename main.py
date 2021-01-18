from tkinter import (Tk, messagebox, filedialog, Text, Menu, Scrollbar, END,
    INSERT, ttk, Canvas, IntVar, Label)
from tkinter.messagebox import *
from tkinter.filedialog import *
import os

class Notepad:
    root = Tk()
    
    #root.geometry('600x500')
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
    status_bar_variable = StringVar()
    
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
        self.file_menu.add_command(label='New', command=self.new_file)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit_app)
        # Edit menu
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_checkbutton(label='Vertical marker',
            onvalue=1, offvalue=0, variable=self.variable_marker,
            command=self.vertical_line)
        #Nested Theme menu
        self.edit_menu.add_cascade(label='Themes', menu=self.theme_edit)
        self.theme_edit.add_command(label="Black", command=self.black_theme)
        self.theme_edit.add_command(label="White", command=self.white_theme)
        # Help menu
        self.help_menu.add_command(label="About", command=self.about)
        
        # Mouse right click popup menu
        self.popup_menu.add_command(label="Copy", command=self.copy)
        self.popup_menu.add_command(label="Paste", command=self.paste)
        self.popup_menu.add_command(label="Cut", command=self.cut)
        self.popup_menu.add_command(label="Undo", command=self.undo)
        self.popup_menu.add_command(label="Redo", command=self.redo)
        self.text_area.bind('<ButtonRelease-3>', self.popup)
        
        # Configure scrollbar
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.text_area.yview,
            cursor="sb_v_double_arrow")
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        
        self.text_area.bind('<Tab>', self.tab)
        # Statusbar
        self.statusbar.grid(sticky='wes')
        self.text_area.bind('<Key>', self.char_count)
        
    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
    
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
    
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
        
    def cut(self):
        self.text_area.event_generate("<<Cut>>")
        
    def paste(self):
        self.text_area.event_generate("<<Paste>>")
        
    def undo(self):
        self.text_area.event_generate("<<Undo>>")
        
    def redo(self):
        self.text_area.event_generate("<<Redo>>")
    
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
        
    def char_count(self, event):
        if event.char == event.keysym or len(repr(event.char)) == 3:
            characters = len(self.text_area.get(1.0, 'end'))
            self.statusbar.config(text=f"Characters: {characters}")
            print(characters)
        elif event.keysym_num == 65288:
            characters = len(self.text_area.get(1.0, 'end-2c'))
            self.statusbar.config(text=f"Characters: {characters}")
            print(characters)
        else:
            pass

    
a = Notepad()
a.run()
