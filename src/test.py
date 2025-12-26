import tkinter as tk

root = tk.Tk()
# Use 'withdraw' to hide the main window immediately
# root.withdraw()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

print(f"Screen width: {width}")
print(f"Screen height: {height}")
while (True):
    i = 1