## main.py
import tkinter as tk
from controller import Controller

def main():
    root = tk.Tk()
    controller = Controller(root)
    root.mainloop()

if __name__ == "__main__":
    main()