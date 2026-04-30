import tkinter as tk
from tkinter.font import Font
import screeninfo
import settings
import dbhandler
from spmg import Rearrangeable, EditableLabel


root = tk.Tk()
root.title("Logic Chain")

# set screen size
if len(screeninfo.get_monitors()) == 2: # two monitors
    root.geometry(f"800x600+{root.winfo_screenwidth()+250}+40")
else:
    root.geometry(f"800x600+250+40")

root.minsize(400, 400)
# root.state('zoomed')
root.config(bg='black')

dbhandler.load()


class PopUp(object):
    """the menu the pops up when mouse right clicks."""

    def __init__(self):
        self.frame = tk.Frame(root, background='gray12')
        root.bind("<Button-1>", lambda e: self.hide())
    
    def clear_frame(self):
        """deletes everything in `self.frame`."""
        for child in self.frame.winfo_children():
            child.pack_forget()

    def show(self, x, y):
        """shows the menu."""
        self.frame.place(anchor='nw', x=x-root.winfo_x()-9, y=y-root.winfo_y()-30)

    def hide(self):
        """hides the menu."""
        self.frame.place_forget()

    def add_button(self, label_text, on_clicked:callable):
        """adds button to `self.frame`."""
        button = tk.Button(
            self.frame,
            text=label_text,
            font=main_font,
            bg='gray10',
            fg='white',
            activebackground='gray8',
            activeforeground='white',
        )
        button.pack(pady=2, padx=2, fill='x')
        
        button.bind("<Enter>", lambda e: button.config(bg='gray14'))
        button.bind("<Leave>", lambda e: button.config(bg='gray10'))
        button.bind("<Button-1>", on_clicked)

    def open_menu(self, buttons:list[tuple[str, callable]], event:tk.Event):
        """something is right clicked.
        `buttons`: a list of tuples where the first element is the text on the button and 
        the second element is the function that runs when the button is clicked."""
        self.clear_frame()

        for label_text, on_clicked in buttons:
            self.add_button(label_text, on_clicked)

        self.show(event.x_root, event.y_root)


class Header(object):
    """the header at the top of the screen."""

    def __init__(self):
        self.frame = tk.Frame(root, height=65, background=settings.opinion_color, padx=4, pady=4)
        self.frame.pack(side='top', fill='x')

        self.menu_button = tk.Button(self.frame, text="Menu", font=main_font, command=menu.toggle_menu)
        self.menu_button.pack(side='left', fill='y')

        self.save_button = tk.Button(self.frame, text="Save", font=main_font)
        self.save_button.pack(side='right', fill='y')

        self.label_frame = tk.Frame(self.frame, background=settings.opinion_color)
        self.label_frame.pack(side='right', fill='both', expand=True, padx=(8, 8))

        placing_kwargs = {'anchor':'center', 'width':None, 'x':0, 'y':0, 'relx':0.5, 'rely':0.5, 'relwidth':1, 'relheight':0.8}
        self.header_text = EditableLabel(self.label_frame, text='Opinion', justify='center', font=main_font, background=settings.opinion_color, placing_kwargs=placing_kwargs)
        self.header_text.place(anchor='center', relx=0.5, rely=0.5, relwidth=1, relheight=0.8)

    def set_label(self, text:str) -> None:
        """set the header label to be `text`."""
        self.header_text.config(text=text)


class Menu(object):
    """The menu that lets you redirect to another page."""

    def __init__(self):
        self.frame = tk.Frame(root, background='gray5')
        # self.frame.pack(side='left', fill='y')

        self.text = tk.Label(self.frame, text="Opinions", background='gray2', padx=4, pady=4, fg='white', font=large_font)
        self.text.pack(side='top')

        self.directory_frame = tk.Frame(self.frame, background='gray5')
        self.directory_frame.pack(side='top', fill='both', expand=True)

        self.directory_menus:list[MenuDirectory] = []
        for id in dbhandler.Directory.top_directories:
            directory:dbhandler.Directory = dbhandler.Directory.top_directories[id]
            self.directory_menus.append(MenuDirectory(directory, self.directory_frame))

    def toggle_menu(self):
        """hides the window if shown, shows window if hidden."""
        if self.frame.winfo_ismapped():
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        """shows the menu."""
        self.frame.pack(side='left', fill='y', after=header.frame)

    def close_menu(self):
        """closes the menu."""
        self.frame.pack_forget()


class MenuDirectory(object):
    """a Directory in the Menu."""

    def __init__(self, directory:dbhandler.Directory, parent_frame:tk.Frame, indentation:int=0):
        self.children_directories:list[MenuDirectory] = []
        """the child directios in `self`."""
        self.directory_data = directory
        """the data of the directory."""
        self.indentation = indentation
        """how far indented the directory is."""
        self.parent_frame:tk.Frame = parent_frame
        """the frame the menu is placed in."""
        
        self.frame = tk.Frame(self.parent_frame, background='gray5')
        self.frame.pack(side='top', fill='x', padx=(indentation*24, 0))

        self.text = tk.Label(self.frame, text=self.directory_data.name, background='gray5', padx=4, fg='white', anchor='w', justify='left', font=main_font)
        self.text.pack(side='left')

        self.caret = tk.Label(self.frame, text='>', background='gray5', padx=8, fg='white', anchor='e', justify='right', font=main_font)
        self.caret.pack(side='right')
        
        self.caret.configure(cursor='hand2')
        self.caret.bind("<Button-1>", lambda e: self.toggle_directory())

        menu_buttons = [("Create Directory", self.create_directory), ("Create Opinion", self.create_opinion)]
        self.caret.bind("<Button-3>", lambda e: pop_up.open_menu(menu_buttons, e))

        self.child_frame = tk.Frame(self.parent_frame, background='gray5')

    def create_directory(self, event:tk.Event):
        """creates a directory in `self`."""
        print(self.directory_data.name, "creating directory")
        dbhandler.create_directory("New Directory", self.directory_data.id)
        self.open_directory()

    def create_opinion(self, event:tk.Event):
        """creates an opinion in `self`."""
        print(self.directory_data.name, "creating opinion")
        dbhandler.create_opinion("", "New Opinion", self.directory_data.id)

    def add_opinion_link(self, opinion:dbhandler.Opinion) -> None:
        """adds opinion link to `child_frame`."""
        opinion_frame = tk.Frame(self.child_frame, background='gray5')
        opinion_frame.pack(side='top', fill='x')

        text = tk.Label(opinion_frame, text=opinion.name, background='gray5', padx=4, fg='white', anchor='w', justify='left', font=underlined_font)
        text.pack(side='left', padx=(24*(self.indentation+1), 0))
        
        text.configure(cursor='hand2')
        text.bind("<Button-1>", lambda e: window.open_table(opinion))

    def toggle_directory(self):
        """closes directory if opened, opens directory if closed."""
        if self.caret.cget('text') == ">":
            self.open_directory()
        else:
            self.close_directory()

    def close_directory(self) -> None:
        """closes directory and deletes its children widgets."""
        self.deletes_child_widgets()
        self.caret.config(text=">")

    def open_directory(self) -> None:
        """opens directory in menu and puts its children in 'frame."""
        self.deletes_child_widgets()
        self.child_frame.pack(side='top', fill='x', after=self.frame)
        self.caret.config(text="⌄")
        
        for child_directory in self.directory_data.children_directories:
            self.children_directories.append(MenuDirectory(child_directory, self.child_frame, self.indentation+1))
        
        for child_opinion in self.directory_data.children_opinions:
            self.add_opinion_link(child_opinion)

    def deletes_child_widgets(self):
        """deletes all children in in `self.child_frame`."""
        for widget in self.child_frame.winfo_children():
            # widget.pack_forget()
            widget.destroy()
        self.child_frame.pack_forget()


class Window(object):
    """The main window of the screen where the logic is."""

    def __init__(self):
        # background will be the color of the border between frames
        self.frame = tk.Frame(root, background='gray40')
        self.frame.pack(side='top', fill='both', expand=True)
        
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
    
    def open_table(self, opinion:dbhandler.Opinion):
        """opens pros/cons table of `opinion`."""
        menu.close_menu()

        self.pros_frame = tk.Frame(self.frame, background='gray10')
        self.cons_frame = tk.Frame(self.frame, background='gray10')

        self.pros_frame.pack(side='left', fill='both', expand=True)
        self.cons_frame.pack(side='right', fill='both', expand=True)

        self.pros_table = ReasonTable(self.pros_frame, 'Pros', opinion.pros)
        self.cons_table = ReasonTable(self.cons_frame, 'Cons', opinion.cons)

        header.set_label(opinion.text)
    

class ReasonTable(Rearrangeable):
    
    def __init__(self, parent:tk.Widget, header_text:str, reasons:list[dbhandler.Opinion]):
        super().__init__(parent=parent, frame_height=settings.font_size*6, starting_frame_data=reasons)
        self.canvas.config(bg='gray25')
        self.scrollable_frame.config(bg="gray25")
        # self.sort_frames()

    def create_frame(self, frame, frame_data:dbhandler.Opinion):
        """creates `reason` box and puts it in `parent`."""
        # create reason to make the code easier to read
        reason:dbhandler.Opinion = frame_data

        header_color = settings.statement_color if reason.is_statement() else settings.opinion_color
        header = tk.Frame(frame, background=header_color)
        header.pack(side='top', fill='x', expand=True)

        delete_button = tk.Button(header, padx=4, background='red', activebackground='#ff7f7f', text='DEL', font=small_font)
        delete_button.pack(side='right', padx=2, pady=2)

        table_button = tk.Button(header, padx=6, background='gray15', activebackground='gray25', fg='white', text='T', font=small_font, command=lambda: window.open_table(reason))
        table_button.pack(side='left', padx=2, pady=2)

        chain_button = tk.Button(header, padx=6, background='gray15', activebackground='gray25', fg='white', text='^', font=small_font)
        chain_button.pack(side='left', padx=2, pady=2)

        text = tk.Text(frame, background='gray20', wrap='word', font=main_font, height=2, fg='white')
        text.insert(tk.END, reason.text)
        text.pack(side='top', fill='x', expand=True)


small_font = Font(family="Consolas", size=int(settings.font_size*0.75), weight="normal")
main_font = Font(family="Consolas", size=int(settings.font_size*1), weight="normal")
large_font = Font(family="Consolas", size=int(settings.font_size*1.5), weight="normal")

underlined_font = Font(family="Consolas", size=int(settings.font_size*1), weight="normal", underline=True)

menu = Menu()
"""the menu used to redirect to a different page."""
header = Header()
"""the header of the screen."""
window = Window()
"""the main window where the current logic is."""
pop_up = PopUp()
"""the menu that appears when somthing is right-clicked."""

window.open_table(dbhandler.Opinion.opinions[1])
# window.open_table(dbhandler.Opinion.opinions[4])


# def test(event):
#     window.pros_table.add_frame(dbhandler.Opinion.opinions[4])

# root.bind("<Return>", test)

# pop_up.directory_clicked()

root.mainloop()
