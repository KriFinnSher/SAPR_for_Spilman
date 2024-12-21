import tkinter as tk
from MainApp import App


if __name__ == "__main__":
    root = tk.Tk()
    app = App.MainApp(root)
    root.mainloop()