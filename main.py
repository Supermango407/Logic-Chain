import tkinter as tk
import setttings
import dbhandler

# root = tk.Tk()
# root.title("Logic Chain")
# root.geometry("800x800+1640+40")
# root.minsize(400, 400)
# root.state('zoomed')
# root.config(bg=setttings.background_color)

dbhandler.load()
print("\nopinions:")
for i in dbhandler.Opinion.opinions:
    opinion = dbhandler.Opinion.opinions[i]
    print(f"  {i}:\t{opinion.text}")

pass
# root.mainloop()
