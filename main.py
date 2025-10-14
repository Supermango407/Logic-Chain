import tkinter as tk
import setttings
import dbhandler

root = tk.Tk()
root.title("Logic Chain")
root.geometry("800x800+1640+40")
root.minsize(400, 400)
root.state('zoomed')
root.config(bg=setttings.background_color)

dbhandler.load()
print("\nstatments:")
for i in dbhandler.statments:
    statment = dbhandler.statments[i]
    print(f"  {i}:\t{statment}")

print("\nopinions:")
for i in dbhandler.opinions:
    opinion = dbhandler.opinions[i]
    print(f"  {i}:\t{opinion.text}")

root.mainloop()
