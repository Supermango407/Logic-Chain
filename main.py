import tkinter as tk
from tkinter.font import Font
import screeninfo
import settings
import dbhandler


root = tk.Tk()
root.title("Logic Chain")

# set screen size
if len(screeninfo.get_monitors()) == 2: # two monitors
    root.geometry(f"800x600+{root.winfo_screenwidth()+250}+40")
else:
    root.geometry(f"800x600+250+40")

root.minsize(400, 400)
root.state('zoomed')
root.config(bg='black')

dbhandler.load()


class Header(object):

    def __init__(self):
        self.frame = tk.Frame(root, height=65, background=settings.opinion_color, padx=4, pady=4)
        self.frame.pack(side='top', fill='x')

        self.menu_button = tk.Button(self.frame, text="Menu", font=main_font, command=menu.toggle_menu)
        self.menu_button.place(anchor='w', rely=0.5)

        self.header_text = tk.Label(self.frame, text='Opinion', font=main_font, background=settings.opinion_color)
        self.header_text.place(anchor='center', relx=0.5, rely=0.5)

    def set_label(self, text:str) -> None:
        """set the header label to be `text`."""
        self.header_text.config(text=text)


class Menu(object):

    def __init__(self):
        self.frame = tk.Frame(root, background='gray5')
        # self.frame.pack(side='left', fill='y')

        self.text = tk.Label(self.frame, text="Opinions", background='gray2', padx=4, pady=4, fg='white', font=large_font)
        self.text.pack(side='top')

        self.directory_frame = tk.Frame(self.frame, background='gray5')
        self.directory_frame.pack(side='top', fill='both', expand=True)

        self.directory_menus:list[DirectoryMenu] = []
        for id in dbhandler.Directory.top_directories:
            directory:dbhandler.Directory = dbhandler.Directory.top_directories[id]
            self.directory_menus.append(DirectoryMenu(directory, self.directory_frame))

    def toggle_menu(self):
        if self.frame.winfo_ismapped():
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        self.frame.pack(side='left', fill='y', after=header.frame)

    def close_menu(self):
        self.frame.pack_forget()


class DirectoryMenu(object):

    def __init__(self, directory:dbhandler.Directory, parrent_frame:tk.Frame, indentation:int=0):
        self.children_directories:list[DirectoryMenu] = []
        self.directory = directory
        self.indentation = indentation
        self.parrent_frame:tk.Frame = parrent_frame
        
        self.frame = tk.Frame(self.parrent_frame, background='gray5')
        self.frame.pack(side='top', fill='x', padx=(indentation*24, 0))

        self.text = tk.Label(self.frame, text=self.directory.name, background='gray5', padx=4, fg='white', anchor='w', justify='left', font=main_font)
        self.text.pack(side='left')

        self.caret = tk.Label(self.frame, text='>', background='gray5', padx=8, fg='white', anchor='e', justify='right', font=main_font)
        self.caret.pack(side='right')
        
        self.caret.configure(cursor='hand2')
        self.caret.bind("<Button-1>", lambda e: self.toggle_directory())

        self.child_frame = tk.Frame(self.parrent_frame, background='gray5')

    def create_opinion(self, opinion:dbhandler.Opinion) -> None:
        """creates opionion link in `child_frame."""
        text = tk.Label(self.child_frame, text=opinion.name, background='gray5', padx=4, fg='white', anchor='w', justify='left', font=underlined_font)
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
        """closes direcory and deletes its children widgets."""
        self.deletes_child_widgets()
        self.caret.config(text=">")

    def open_directory(self) -> None:
        """opens directory in menu and puts its children in 'frame."""
        self.deletes_child_widgets()
        self.child_frame.pack(side='top', fill='x', after=self.frame)
        self.caret.config(text="⌄")
        for child in self.directory.children:
            if type(child) == dbhandler.Directory:
                self.children_directories.append(DirectoryMenu(child, self.child_frame, self.indentation+1))
            elif type(child) == dbhandler.Opinion:
                self.create_opinion(child)

    def deletes_child_widgets(self):
        """delets all children in in `self.child_frame`."""
        for widget in self.child_frame.winfo_children():
            # widget.pack_forget()
            widget.destroy()
        self.child_frame.pack_forget()


class Window(object):


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

        self.pros_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 1))
        self.cons_frame.grid(row=0, column=1, sticky='nsew', padx=(1, 0))

        self.pros_table = ReasonTable(self.pros_frame, 'Pros', opinion.pros)
        self.cons_table = ReasonTable(self.cons_frame, 'Cons', opinion.cons)

        header.set_label(opinion.text)
    

class ReasonTable(object):

    def __init__(self, parrent:tk.Widget, header_text:str, reasons:list[dbhandler.Opinion]):
        self.label = tk.Label(parrent, text=header_text, background='gray10', fg='white', font=large_font)
        self.label.pack(side='top', fill='x')

        self.canvas = tk.Canvas(parrent, background='gray15', borderwidth=0, highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)

        self.scrollbar = tk.Scrollbar(parrent, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas, background='gray15')
        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfig(self.scrollable_frame_id, width=event.width))
        self.scrollable_frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.scrollable_frame.bind("<MouseWheel>", self.on_mouse_wheel)

        for reason in reasons:
            self.add_reason(self.scrollable_frame, reason)

    def add_reason(self, parrent:tk.Widget, reason:dbhandler.Opinion):
        """creates `reason` box and puts it in `parrent`."""
        frame = tk.Frame(parrent, background='gray10')
        frame.pack(side='top', fill='x', padx=(10, 10), pady=(10, 0))
        frame.bind("<MouseWheel>", self.on_mouse_wheel)

        header_color = settings.statment_color if reason.is_statment() else settings.opinion_color
        header = tk.Frame(frame, background=header_color)
        header.pack(side='top', fill='x', expand=True)
        header.bind("<MouseWheel>", self.on_mouse_wheel)

        delete_button = tk.Button(header, padx=4, background='red', activebackground='#ff7f7f', text='DEL', font=small_font)
        delete_button.pack(side='right')
        delete_button.bind("<MouseWheel>", self.on_mouse_wheel)

        table_button = tk.Button(header, padx=6, background='gray15', activebackground='gray25', fg='white', text='T', font=small_font, command=lambda: window.open_table(reason))
        table_button.pack(side='left')
        table_button.bind("<MouseWheel>", self.on_mouse_wheel)

        chain_button = tk.Button(header, padx=6, background='gray15', activebackground='gray25', fg='white', text='^', font=small_font)
        chain_button.pack(side='left')
        chain_button.bind("<MouseWheel>", self.on_mouse_wheel)

        text = tk.Text(frame, background='gray20', wrap='word', font=main_font, height=2, fg='white')
        text.insert(tk.END, reason.text)
        text.pack(side='top', fill='x', expand=True)
        text.bind("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, event:tk.Event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")


small_font = Font(family="Consolas", size=int(settings.font_size*0.5), weight="normal")
main_font = Font(family="Consolas", size=int(settings.font_size*1), weight="normal")
large_font = Font(family="Consolas", size=int(settings.font_size*1.5), weight="normal")

underlined_font = Font(family="Consolas", size=int(settings.font_size*1), weight="normal", underline=True)

menu = Menu()
header = Header()
window = Window()

window.open_table(dbhandler.Opinion.opinions[1])
# window.open_table(dbhandler.Opinion.opinions[4])

root.mainloop()
