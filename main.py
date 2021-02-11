import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox
import os

class Notepad:
    root = tk.Tk()
    Width = 800
    Height = 600
    
    text_area = tk.Text(root, undo=True, wrap='char')
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu =tk.Menu(menu_bar, tearoff=0)
    theme_edit = tk.Menu(edit_menu, tearoff=0)
    help_menu = tk.Menu(menu_bar, tearoff=0)
    popup_menu = tk.Menu(root, tearoff=0)
    
    scrollbar = tk.Scrollbar(root)
    file = None
    
    tab_width = 4
    
    variable_marker = tk.BooleanVar()
    variable_theme = tk.IntVar()
    
    canvas = tk.Canvas(text_area, width=1, height=Height,
            highlightthickness=0, bg='lightsteelblue3')
            
    statusbar = tk.Label(root,
        text=f"Total Lines: 0 | Col: 0 | Symbols: 0",
        relief=tk.FLAT, anchor='e')
    left_bar = tk.Label(root, relief=tk.FLAT, width=0)
    
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
        self.root.grid_columnconfigure(1, weight=1)
        # Make textarea size as window
        self.text_area.grid(column=1, row=0, sticky='nsew')
        
        # Configure scrollbar
        self.scrollbar.grid(column=2, row=0, sticky='ns')
        self.scrollbar.config(command=self.text_area.yview,
            cursor="sb_v_double_arrow")
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        # Left bar
        self.left_bar.grid(column=0, row=0, sticky='ns')
        
        # Statusbar
        self.statusbar.grid(column=0, columnspan=3, row=1, sticky='wes')
        
        ## Menu GUI
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
        # Nested Theme menu
        self.edit_menu.add_cascade(label='Color theme', menu=self.theme_edit)
        self.theme_edit.add_checkbutton(label="Black", onvalue=1, offvalue=0,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Light Grey", onvalue=2,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Pale Turquoise", onvalue=3,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Snow", onvalue=4,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Azure", onvalue=5,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Navajo White", onvalue=6,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Lavender", onvalue=7,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Misty Rose", onvalue=8,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Dark Slate Gray", onvalue=9,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Dim Gray", onvalue=10,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Khaki", onvalue=11,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Deep Sky Blue", onvalue=12,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Aquamarine", onvalue=13,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Blue", onvalue=14,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Midnight Blue", onvalue=15,
            variable=self.variable_theme, command=self.theme_activate)
        self.theme_edit.add_checkbutton(label="Cyber Dark", onvalue=16,
            variable=self.variable_theme, command=self.theme_activate)
        
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
        self.text_area.bind('<Tab>', self.tab)
        self.text_area.bind('<Shift-Tab>', self.shift_tab)
        self.text_area.bind('<ButtonRelease-3>', self.popup)
        self.text_area.bind('<Control-r>', self.redo)
        self.text_area.bind('<Control-z>', self.undo)
        self.text_area.bind('<Control-a>', self.select_all)
        self.text_area.bind('<Control-s>', self.save_file)
        self.text_area.bind('<Control-Alt-s>', self.save_file_as)
        self.text_area.bind('<Control-n>', self.new_file)
        self.text_area.bind('<Control-o>', self.open_file)
        # Vertical line auto resize
        self.text_area.bind('<Configure>', self.vertical_line)
        
    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
    
    def new_file(self, event=None):
        self.root.title("Untitled - Notepad")
        self.file = None
        self.text_area.delete(0.0, tk.END)
        
    def open_file(self, event=None):
        self.file = tkFileDialog.askopenfilename(defaultextension=".txt",
            filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')])
        if self.file == "":
            self.file = None
        else:
            self.root.title(os.path.basename(self.file) + " - Notepad")
            self.text_area.delete(0.0, tk.END)
            file = open(self.file, 'r')
            self.text_area.insert(0.0, file.read())
            file.close()

    def save_file_as(self, event=None):
        tkFileDialog.asksaveasfilename(initialfile='Untitled.txt', 
            defaultextension='.txt', filetypes=[('All Files', '*.*'),
            ('Text Documents', '*.txt')])
            
    def save_file(self, event=None):
        if self.file is not None and self.file != "":
            with open(self.file, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))
            self.root.title(os.path.basename(self.file))
        else:
            self.save_file_as()
                            
    def quit_app(self):
        self.save_file()
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
        tkMessageBox.showinfo("Notepad", "Simple but Good :)")
    
    def run(self):
        self.root.mainloop()
        
    def tab(self, arg):
        self.text_area.insert(tk.INSERT, " " * self.tab_width)
        return 'break'
    
    def shift_tab(self, event=None):
        previous_characters = self.text_area.get(
            "insert -%dc" % self.tab_width, tk.INSERT)
        if previous_characters == " " * self.tab_width:
            self.text_area.delete("insert-%dc" % self.tab_width, tk.INSERT)
        return "break"
       
    def theme_activate(self):
        if self.variable_theme.get() == 0:
            self.text_area.config(bg='SystemWindow', fg='SystemWindowText',
                insertbackground='SystemWindowText')
        elif self.variable_theme.get() == 1:
            self.text_area.config(bg='black', fg='white',
                insertbackground='white')
        elif self.variable_theme.get() == 2:
            self.text_area.config(bg='light grey', fg='black',
                insertbackground='white')
        elif self.variable_theme.get() == 3:
            self.text_area.config(bg='paleturquoise1', fg='black',
                insertbackground='black')
        elif self.variable_theme.get() == 4:
            self.text_area.config(bg='snow', fg='black',
                insertbackground='black')
        elif self.variable_theme.get() == 5:
            self.text_area.config(bg='azure', fg='black',
                insertbackground='black')
        elif self.variable_theme.get() == 6:
            self.text_area.config(bg='navajo white', fg='black',
                insertbackground='black')
        elif self.variable_theme.get() == 7:
            self.text_area.config(bg='lavender', fg='black',
                insertbackground='black')
        elif self.variable_theme.get() == 8:
            self.text_area.config(bg='misty rose', fg='black',
                insertbackground='black')
        elif self.variable_theme.get() == 9:
            self.text_area.config(bg='dark slate gray', fg='linen',
                insertbackground='white')
        elif self.variable_theme.get() == 10:
            self.text_area.config(bg='dim gray', fg='ghost white',
                insertbackground='white')
        elif self.variable_theme.get() == 11:
            self.text_area.config(bg='khaki', fg='deepskyblue4',
                insertbackground='white')
        elif self.variable_theme.get() == 12:
            self.text_area.config(bg='deepskyblue4', fg='light cyan',
                insertbackground='white')
        elif self.variable_theme.get() == 13:
            self.text_area.config(bg='aquamarine', fg='red4',
                insertbackground='black')
        elif self.variable_theme.get() == 14:
            self.text_area.config(bg='blue4', fg='white',
                insertbackground='white')
        elif self.variable_theme.get() == 15:
            self.text_area.config(bg='midnight blue', fg='white',
                insertbackground='white')
        elif self.variable_theme.get() == 16:
            self.text_area.config(bg='#1f1f2e', fg='cyan',
                insertbackground='white')
        else:
            return 'Error'
       
    def vertical_line(self, event=None):
        if self.variable_marker.get() == 1:
            self.canvas.place(x=640, height=self.root.winfo_height())
        elif self.variable_marker.get() == 0:
            self.canvas.place_forget()  # Unmap widget
        else:
            return "Error"
            
    def text_area_modified(self, event=None):
        line=self.text_area.count('1.0', 'end', 'displaylines')
        col=str(len(self.text_area.get('insert linestart','insert lineend')))
        symb = str(len(self.text_area.get(1.0, 'end-1c')))
        if self.text_area.edit_modified():
            self.statusbar.config(
            text=f"Total Lines: {line[0]} | Col: {col} | Symbols: {symb}")
        self.text_area.edit_modified(False)
        
notepad = Notepad()
notepad.run()
