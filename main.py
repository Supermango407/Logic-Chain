import tkinter as tk
from tkinter.font import Font
import screeninfo
import settings
import dbhandler


# root = tk.Tk()
# root.title("Logic Chain")

# set screen size
if len(screeninfo.get_monitors()) == 2: # two monitors
    # root.geometry(f"800x800+{root.winfo_screenwidth()+250}+40")
else:
    root.geometry(f"800x800+250+40")

# root.minsize(400, 400)
# root.state('zoomed')
# root.config(bg='black')

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
        self.frame = tk.Frame(root, background=settings.header_color, padx=4, pady=4)
        self.frame.pack(side='top', fill='x')

        self.menu_button = tk.Button(self.frame, text="Menu", font=main_font, command=menu.toggle)
        self.menu_button.pack(side='left')

        self.header_text = tk.Label(self.frame, text='Opinion', font=header_font, background=settings.header_color)
        self.header_text.pack(side='top', expand=True)


class Menu(object):

    def __init__(self):
        self.frame = tk.Frame(root, background=settings.menu_color)
        # self.frame.pack(side='left', fill='y')

        self.text = tk.Label(self.frame, text="Opinions", padx=4, pady=4, fg='white', background=settings.menu_color, font=main_font)
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


class Window():

    def __init__(self):
        self.frame = tk.Frame(root, background=settings.border_color)
        self.frame.pack(side='top', fill='both', expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.pros_frame = tk.Frame(self.frame, background=settings.background_color, padx=1, pady=1)
        self.cons_frame = tk.Frame(self.frame, background=settings.background_color, padx=1, pady=1)

        self.pros_frame.pack(side='left', fill='both', expand=True, padx=1, pady=1)
        self.cons_frame.pack(side='right', fill='both', expand=True, padx=1, pady=1)
    
    def open_table(self, opinion:dbhandler.Opinion):
        """opens pros/cons table of `opinion`."""
        self.pros_frame = tk.Frame(self.frame, background='blue', borderwidth=2)
        self.cons_frame = tk.Frame(self.frame, background='red', borderwidth=2)

        self.pros_frame.place(anchor='w', height=1, width=0.4)
        self.cons_frame.place(anchor='e', height=1, width=0.4)


main_font = Font(family="Consolas", size=int(settings.font_size), weight="normal")
header_font = Font(family="Consolas", size=int(settings.font_size*1.5), weight="normal")

menu = Menu()
header = Header()
window = Window()

# window.open_table(dbhandler.opinions[1])

pass
# root.mainloop()
