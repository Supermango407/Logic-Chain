import tkinter as tk
from tkinter.font import Font
import screeninfo
import settings
import dbhandler


root = tk.Tk()
root.title("Logic Chain")

# set screen size
if len(screeninfo.get_monitors()) == 2: # two monitors
    root.geometry(f"800x800+{root.winfo_screenwidth()+250}+40")
else:
    root.geometry(f"800x800+250+40")

root.minsize(400, 400)
root.state('zoomed')
root.config(bg='black')

dbhandler.load()
# print("\nstatments:")
# for i in dbhandler.statments:
#     statment = dbhandler.statments[i]
#     print(f"  {i}:\t{statment}")

# print("\nopinions:")
# for i in dbhandler.opinions:
    # opinion = dbhandler.opinions[i]
    # print(f"  {i}:\t{opinion.text}")


class Header(object):

    def __init__(self):
        self.frame = tk.Frame(root, background=settings.opinion_color, padx=4, pady=4)
        self.frame.pack(side='top', fill='x')

        self.menu_button = tk.Button(self.frame, text="Menu", font=main_font, command=menu.toggle)
        self.menu_button.pack(side='left')

        self.header_text = tk.Label(self.frame, text='Opinion', font=large_font, background=settings.opinion_color)
        self.header_text.pack(side='top', expand=True)


class Menu(object):

    def __init__(self):
        self.frame = tk.Frame(root, background='gray5')
        # self.frame.pack(side='left', fill='y')

        self.text = tk.Label(self.frame, text="Opinions", background='gray5', padx=4, pady=4, fg='white', font=main_font)
        self.text.pack(side='top')

    def toggle(self):
        if self.frame.winfo_ismapped():
            self.close()
        else:
            self.open()

    def open(self):
        self.frame.pack(side='left', fill='y', after=header.frame)

    def close(self):
        self.frame.pack_forget()


class Window(object):

    def __init__(self):
        # background will be the color of the border between frames
        self.frame = tk.Frame(root, background='gray40')
        self.frame.pack(side='top', fill='both', expand=True)
    
    def open_table(self, opinion:dbhandler.Opinion):
        """opens pros/cons table of `opinion`."""
        self.pros_frame = tk.Frame(self.frame, background='gray10')
        self.cons_frame = tk.Frame(self.frame, background='gray10')

        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.pros_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 1))
        self.cons_frame.grid(row=0, column=1, sticky='nsew', padx=(1, 0))

        self.pros_label = tk.Label(self.pros_frame, text='Pros', background='gray10', fg='white', font=large_font)
        self.pros_label.pack(side='top', fill='x')
        self.cons_label = tk.Label(self.cons_frame, text='Cons', background='gray10', fg='white', font=large_font)
        self.cons_label.pack(side='top', fill='x')

        self.pros_opinions_frame = tk.Frame(self.pros_frame, background='gray15')
        self.pros_opinions_frame.pack(side='top', fill='both', expand=True)
        self.cons_opinions_frame = tk.Frame(self.cons_frame, background='gray15')
        self.cons_opinions_frame.pack(side='top', fill='both', expand=True)
        
        self.add_opinions_frames(self.pros_opinions_frame, opinion.pros)
        self.add_opinions_frames(self.cons_opinions_frame, opinion.cons)
    
    def add_opinions_frames(self, parrent:tk.Widget, opinions:list[dbhandler.Opinion]):
        """adds frames for `opinions` to `parrent`."""
        for opinion in opinions:
            frame = tk.Frame(parrent, background='gray10')
            frame.pack(side='top', fill='x', padx=(10, 10), pady=(10, 0))

            header_color = settings.statment_color if opinion.is_statment() else settings.opinion_color
            header = tk.Frame(frame, background=header_color)
            header.pack(side='top', fill='x', expand=True)

            delete_button = tk.Button(header, background='red', activebackground='#ff7f7f', text='DEL', font=small_font)
            delete_button.pack(side='right')

            text = tk.Text(frame, background='gray20', wrap='word', font=main_font, height=2, fg='white')
            text.insert(tk.END, opinion.text)
            text.pack(side='top', fill='x', expand=True)


small_font = Font(family="Consolas", size=int(settings.font_size*0.5), weight="normal")
main_font = Font(family="Consolas", size=int(settings.font_size*1), weight="normal")
large_font = Font(family="Consolas", size=int(settings.font_size*1.5), weight="normal")

menu = Menu()
header = Header()
window = Window()

window.open_table(dbhandler.Opinion.opinions[1])
# window.open_table(dbhandler.Opinion.opinions[4])

root.mainloop()
