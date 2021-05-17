import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox

from text_widget import TextWidget
from line_enumerator import LineEnumerator

import os
import ctypes


class Notepad:
    root = tk.Tk()
    Width = 800
    Height = 600
    
    text_area = TextWidget(root, undo=True, wrap='none')
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    customize_menu = tk.Menu(menu_bar, tearoff=0)
    vertical_marker_menu = tk.Menu(customize_menu, tearoff=0)
    line_bar_menu = tk.Menu(customize_menu, tearoff=0)
    statusbar_menu = tk.Menu(customize_menu, tearoff=0)
    theme_edit = tk.Menu(customize_menu, tearoff=0)
    s_bars_menu = tk.Menu(customize_menu, tearoff=0)
    help_menu = tk.Menu(menu_bar, tearoff=0)
    popup_menu = tk.Menu(root, tearoff=0)

    search_box_label = tk.Label(text_area, highlightthickness=0)
    
    scrollbar_y = tk.Scrollbar(root)
    scrollbar_x = tk.Scrollbar(root, orient='horizontal')

    filename = ''
    filename_var = ''
    file_options = [('All Files', '*.*'), ('Python Files', '*.py'),
                ('Text Document', '*.txt')]
    
    tab_width = 4
    
    variable_marker = tk.IntVar()
    variable_theme = tk.IntVar()
    variable_line_bar = tk.IntVar()
    variable_statusbar = tk.IntVar()
    variable_hide_menu = tk.BooleanVar()
    variable_statusbar_hide = tk.BooleanVar()
    variable_line_bar_hide = tk.BooleanVar()
    variable_search_box = tk.BooleanVar()
    
    canvas_line = tk.Canvas(text_area, width=1, height=Height,
            highlightthickness=0, bg='lightsteelblue3')
            
    statusbar = tk.Label(root, text=f"Line: 1 | Col: 0 | Symbols: 0",
        relief=tk.FLAT, anchor='e', highlightthickness=0)
    line_count_bar = LineEnumerator(width=27, highlightthickness=0)

    def __init__(self):
        self.root.title("Untitled")

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

        # Set DPI Awareness  (Windows 10 and 8)
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
        
        # Configure Yscrollbar
        self.text_area.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.config(command=self.text_area.yview,
            cursor="sb_v_double_arrow")
        self.scrollbar_y.grid(column=2, row=0, sticky='ns')
        # Configure Xscrollbar
        self.text_area.configure(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.config(command=self.text_area.xview,
            cursor="sb_h_double_arrow")
        self.scrollbar_x.grid(column=1, row=1, sticky='ew')

        # Line count bar
        self.line_count_bar.attach(self.text_area)
        self.line_count_bar.grid(column=0, row=0, sticky='ns')

        # Statusbar
        self.statusbar.grid(column=0, columnspan=3, row=2, sticky='wes')
        
        ## Menu GUI
        self.root.config(menu=self.menu_bar)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label='Customize', menu=self.customize_menu)
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
        self.edit_menu.add_command(label="Search", accelerator='Ctrl+F',
            command=self.search_box)
        self.edit_menu.add_command(label="Find next", command=self.next_match)

        # Customize menu
        self.customize_menu.add_cascade(label='Vertical marker',
            menu=self.vertical_marker_menu)
        self.customize_menu.add_cascade(label='Color theme',
            menu=self.theme_edit)
        self.customize_menu.add_cascade(label="Line bar color",
            menu=self.line_bar_menu)
        self.customize_menu.add_cascade(label="Statusbar color",
            menu=self.statusbar_menu)
        self.customize_menu.add_cascade(label='StatusBars',
            menu=self.s_bars_menu)

        # StatusBars hide option
        self.s_bars_menu.add_command(label='Hide Bottom',
            command=self.statusbar_remove)
        self.s_bars_menu.add_command(label='Hide LeftBar',
            command=self.line_bar_remove)

        # Status bar color
        self.statusbar_menu.add_checkbutton(label='LightSteelBlue', onvalue=1,
            offvalue=0, variable=self.variable_statusbar,
            command=self.statusbar_color)
        self.statusbar_menu.add_checkbutton(label='Yellow', onvalue=2,
            offvalue=0, variable=self.variable_statusbar,
            command=self.statusbar_color)
        self.statusbar_menu.add_checkbutton(label='Dodger blue', onvalue=3,
            offvalue=0, variable=self.variable_statusbar,
            command=self.statusbar_color)
        self.statusbar_menu.add_checkbutton(label='Indian red', onvalue=4,
            offvalue=0, variable=self.variable_statusbar,
            command=self.statusbar_color)

        # Left bar color
        self.line_bar_menu.add_checkbutton(label='LightSteelBlue', onvalue=1,
            offvalue=0, variable=self.variable_line_bar,
            command=self.line_bar_color)
        self.line_bar_menu.add_checkbutton(label='Yellow', onvalue=2,
            offvalue=0, variable=self.variable_line_bar,
            command=self.line_bar_color)
        self.line_bar_menu.add_checkbutton(label='Dodger blue', onvalue=3,
            offvalue=0, variable=self.variable_line_bar,
            command=self.line_bar_color)
        self.line_bar_menu.add_checkbutton(label='Indian red', onvalue=4,
            offvalue=0, variable=self.variable_line_bar,
            command=self.line_bar_color)

        # Vertical marker
        self.vertical_marker_menu.add_checkbutton(label="80", onvalue=1,
            offvalue=0, variable=self.variable_marker,
            command=self.vertical_line)
        self.vertical_marker_menu.add_checkbutton(label="120", onvalue=2,
            variable=self.variable_marker, command=self.vertical_line)

        # Nested Theme menu
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
        self.popup_menu.add_command(label='Hide menu',
            command=self.hide_menu, accelerator='Ctrl+H')

        # Button bind
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
        self.text_area.bind('<Control-h>', self.hide_menu)
        self.root.bind('<Control-f>', self.search_box)

        # Vertical line auto resize
        self.text_area.bind('<Configure>', self.vertical_line)

        # Statusbar count. Manual event. Line bar count
        self.text_area.bind("<<IcursorModify>>", self.icursor_modify)
        self.text_area.bind("<<Configure>>", self.icursor_modify)

        # Search entry box
        self.search_entry = tk.Entry(self.search_box_label, bg='light cyan', bd=4,
            width=35, justify=tk.CENTER)
        self.search_entry.grid(column=1, row=0, columnspan=1)
        self.search_button = tk.Button(self.search_box_label, text='Search', bd=1,
            command=self.find_match, cursor='arrow')
        self.search_button.grid(column=0, row=0, columnspan=1)

    def search_box(self, event=None):
        """Make Search box appear inside text area"""
        if self.variable_search_box.get() == True:
            self.search_box_label.place_forget()
            self.variable_search_box.set(False)
            self.search_entry.unbind('<Return>')
        elif self.variable_search_box.get() == False:
            self.search_box_label.place(bordermode=tk.INSIDE,
                width=self.Width/3, relx=1.0, rely=0.0, anchor='ne')
            self.variable_search_box.set(True)
            self.search_entry.focus_set()
            self.search_entry.bind('<Return>', self.find_match)
        else:
            return None

    def find_match(self, event=None):
        """Search for match of words or symbols inside text area"""
        self.text_area.tag_remove('find_match', '1.0', tk.END)
        _search = self.search_entry.get()

        if _search:
            _index = '1.0'
            while True:
                _index = self.text_area.search(_search, _index,
                    nocase=True, stopindex=tk.END)
                if not _index:
                    break
                _last_index = '%s+%dc' % (_index, len(_search))
                self.text_area.tag_add('find_match', _index, _last_index)
                _index = _last_index
            self.text_area.tag_config('find_match', background='yellow',
                foreground='black')
        self.search_entry.focus_set()
        return "break"

    def next_match(self, event=None):
        """
        Move cursor to next match and focus it.
        https://stackoverflow.com/a/44164144
        """
        self.text_area.focus_set()
        # move cursor to beginning of current match
        while (self.text_area.compare("insert", "<", "end") and
            "find_match" in self.text_area.tag_names("insert")):
                self.text_area.mark_set("insert", "insert+1c")
        # find next character with the tag
        next_match = self.text_area.tag_nextrange("find_match", "insert")
        if next_match:
            self.text_area.mark_set("insert", next_match[0])
            self.text_area.see("insert")
        # prevent default behavior, in case this was called
        # via a key binding
        return "break"

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
    
    def new_file(self, event=None):
        self.root.title(self.filename)
        self.filename = ''
        self.text_area.delete(0.0, tk.END)
        
    def open_file(self, event=None):
        try:
            self.filename = tkFileDialog.askopenfilename(defaultextension=".txt",
                filetypes=self.file_options)
            if self.filename is not None:
                with open(self.filename, 'r') as data:
                    self.root.title(os.path.basename(self.filename))
                    self.text_area.delete(0.0, tk.END)
                    self.text_area.insert(0.0, data.read())
        except FileNotFoundError:
            return None

    def save_file_as(self, event=None):
        self.filename_var = self.filename
        try:
            self.filename = tkFileDialog.asksaveasfilename(
                initialfile=self.root.title().strip("*"),
                defaultextension='.txt', filetypes=self.file_options)
            if self.filename == '':
                self.filename = self.filename_var
            else:
                with open(self.filename, 'w') as data:
                    data.write(self.text_area.get(1.0, tk.END))
                    self.root.title(os.path.basename(self.filename))
        except Exception as e:
            raise e
                
    def save_file(self, event=None):
        if self.filename != None and self.filename != "":
            with open(self.filename, 'w') as note:
                    note.write(self.text_area.get(1.0, tk.END))
            self.root.title(os.path.basename(self.filename))
        elif self.filename == None or self.filename =='':
            self.save_file_as()
        else:
            return "Error"

    def quit_app(self):
        self.save_file()
        self.root.destroy()
    
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
        
    def cut(self, event=None):
        self.text_area.event_generate("<<Cut>>")
        
    def paste(self, event=None):
        self.text_area.event_generate("<<Paste>>")
        return 'break'
        
    def undo(self, event=None):
        self.text_area.event_generate("<<Undo>>")
        
    def redo(self, event=None):
        self.text_area.event_generate("<<Redo>>")
        
    def select_all(self, event=None):
        self.text_area.event_generate("<<SelectAll>>")
    
    def about(self):
        tkMessageBox.showinfo("Notepad", "Simple but Good :)")
    
    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            raise e
        
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
        if self.variable_marker.get() == 0:
            self.canvas_line.place_forget()  # Unmap widget
        elif self.variable_marker.get() == 1:
            self.canvas_line.place(x=640, height=self.root.winfo_height())
        elif self.variable_marker.get() == 2:
            self.canvas_line.place(x=960, height=self.root.winfo_height())
        else:
            return "Error"          

    def icursor_modify(self, event):
        line, col = self.text_area.index("insert").split(".")
        symb = str(len(self.text_area.get(1.0, 'end-1c')))
        self.statusbar.config(
            text=f"Line: {line} | Col: {col} | Symbols: {symb}")
        self.line_count_bar.redraw()
        # Need to think
        if self.text_area.edit_modified():
            self.root.title(os.path.basename(self.filename) + '*')
    
    def line_bar_color(self, event=None):
        if self.variable_line_bar.get() == 0:
            self.line_count_bar.config(bg='SystemButtonFace')
        elif self.variable_line_bar.get() == 1:
            self.line_count_bar.config(bg='lightsteelblue3')
        elif self.variable_line_bar.get() == 2:
            self.line_count_bar.config(bg='yellow')
        elif self.variable_line_bar.get() == 3:
            self.line_count_bar.config(bg='dodger blue')
        elif self.variable_line_bar.get() == 4:
            self.line_count_bar.config(bg='Indian red')
        else:
            return "Error"
    
    def statusbar_color(self, event=None):
        if self.variable_statusbar.get() == 0:
            self.statusbar.config(bg='SystemButtonFace')
        elif self.variable_statusbar.get() == 1:
            self.statusbar.config(bg='lightsteelblue3')
        elif self.variable_statusbar.get() == 2:
            self.statusbar.config(bg='yellow')
        elif self.variable_statusbar.get() == 3:
            self.statusbar.config(bg='dodger blue')
        elif self.variable_statusbar.get() == 4:
            self.statusbar.config(bg='Indian red')
        else:
            return "Error"

    def hide_menu(self, event=None):
        fake_menu_bar = tk.Menu(self.root)
        if self.variable_hide_menu.get() == False:
            self.root.config(menu=fake_menu_bar)
            self.variable_hide_menu.set(True)
        elif self.variable_hide_menu.get() == True:
            self.root.config(menu=self.menu_bar)
            self.variable_hide_menu.set(False)
        else:
            return None
    
    def statusbar_remove(self):
        if self.variable_statusbar_hide.get() == False:
            self.statusbar.grid_forget()
            self.variable_statusbar_hide.set(True)
        elif self.variable_statusbar_hide.get() == True:
            self.statusbar.grid(column=0, columnspan=3, row=1, sticky='wes')
            self.variable_statusbar_hide.set(False)
        else:
            return None
    
    def line_bar_remove(self):
        if self.variable_line_bar_hide.get() == False:
            self.line_count_bar.grid_forget()
            self.variable_line_bar_hide.set(True)
        elif self.variable_line_bar_hide.get() == True:
            self.line_count_bar.grid(column=0, row=0, sticky='ns')
            self.variable_line_bar_hide.set(False)
        else:
            return None

notepad = Notepad()
notepad.run()
