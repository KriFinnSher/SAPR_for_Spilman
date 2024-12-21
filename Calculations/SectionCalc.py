import tkinter as tk
from tkinter import ttk, messagebox
from Calculations import MainCalc
from MainApp import Checks


def show_section_window(data):
    def get_section(num, x_val):
        num = int(num.get().split()[1])

        x_val = x_val.get()
        if x_val == "":
            messagebox.showinfo("Ошибка", "Пожалуйста, введите координату стержня.")
            return

        if float(x_val) > float(data['L'][num-1]):
            messagebox.showinfo("Ошибка", "Пожалуйста, введите корректную координату стержня.")
            return

        u, n, s = MainCalc.GET_SECTION(data, num, float(x_val))

        uLabel.config(text=f'Значение U(x): {u}')
        nLabel.config(text=f'Значение N(x): {n}')
        sLabel.config(text=f'Значение σ(x): {s}')


    sectionWindow = tk.Toplevel()
    sectionWindow.title("Расчет сечения")
    sectionWindow.geometry('380x150')
    sectionWindow.resizable(False, False)
    sectionWindow.config(bg="#048dba")

    mainFrame = tk.Frame(sectionWindow)
    mainFrame.config(bg="#048dba")
    mainFrame.grid(column=0, row=0, padx=5, pady=5)
    t = mainFrame.register(Checks.check_2)

    vals = []
    for i, l in enumerate(data['L'], start=1):
        vals.append(f'Стержень {i} [0;{l}]')

    numLabel = tk.Label(mainFrame, text='Выберите стержень:')
    numLabel.grid(column=1, row=0, padx=5, pady=5)
    numLabel.config(bg="#048dba")

    steelCB = ttk.Combobox(mainFrame, values=vals, width=12, state='readonly')
    steelCB.grid(column=2, row=0, padx=5, pady=5)
    steelCB.current(0)


    x_label = tk.Label(mainFrame, text='Координата стержня:')
    x_label.grid(column=1, row=1, padx=5, pady=5)
    x_label.config(bg="#048dba")

    x_entry = tk.Entry(mainFrame, width=5, validate='all', validatecommand=(t, '%P'))
    x_entry.grid(column=2, row=1, padx=5, pady=5)

    res_button = tk.Button(mainFrame, text='Расчет', command=lambda: get_section(steelCB, x_entry), width=10)
    res_button.grid(column=3, row=0, padx=5, pady=5)
    res_button.configure(bg="#20bff5", activebackground="#76d5f5")

    nLabel = tk.Label(mainFrame, text=f'Значение N(x):')
    nLabel.grid(column=3, row=1, padx=5, pady=5)
    nLabel.config(bg="#048dba")

    uLabel = tk.Label(mainFrame, text=f'Значение U(x):')
    uLabel.grid(column=3, row=2, padx=5, pady=5)
    uLabel.config(bg="#048dba")

    sLabel = tk.Label(mainFrame, text=f'Значение σ(x):')
    sLabel.grid(column=3, row=3, padx=5, pady=5)
    sLabel.config(bg="#048dba")