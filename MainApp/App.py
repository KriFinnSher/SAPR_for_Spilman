import json
import tkinter as tk
from collections import defaultdict
from tkinter import filedialog

from MainApp import Checks, Visual
from Calculations import MainCalc, SectionCalc


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="#048dba")
        self.root.title("САПР")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        self.fields = []
        self.input_data = defaultdict(list)
        self.npn = (self.root.register(Checks.check_1), '%P')
        self.rpn = (self.root.register(Checks.check_2), '%P')
        self.rn = (self.root.register(Checks.check_3), '%P')

        self.create_widgets()

    def create_widgets(self):
        self.create_steel_section()
        self.create_support_section()
        self.create_file_section()
        self.create_calculation_section()
        self.create_construction_section()

    def create_steel_section(self):
        steel_frame = tk.LabelFrame(self.root, text="Стержни", padx=5, pady=5)
        steel_frame.place(relx=0.02, rely=0.02, relwidth=0.95, relheight=0.3)
        steel_frame.configure(bg="#76d5f5")

        canvas = tk.Canvas(steel_frame)
        canvas.configure(bg="#76d5f5")
        scrollbar = tk.Scrollbar(steel_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.configure(bg="#76d5f5")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        clear_button = tk.Button(self.scrollable_frame, text="Очистить ввод", background='#e83140', activebackground='#f05b67', command=self.clear_all)
        clear_button.grid(row=0, column=3, padx=5, pady=5, columnspan=2, sticky="w")

        add_button = tk.Button(self.scrollable_frame, text="Добавить стержень", background='#048dba', activebackground='#76d5f5', command=self.add_steel)
        add_button.grid(row=0, column=4, padx=5, pady=5, columnspan=2, sticky="e")

        labels = ["Узел (0), F", "A, м²", "L, м", "E, Па", "[σ], Па", "q, Н/м", "Узел (L), F"]
        for i, text in enumerate(labels):
            a = tk.Label(self.scrollable_frame, text=text)
            a.grid(row=1, column=i + 1, padx=5, pady=5)
            a.configure(bg="#76d5f5")

        a = tk.Label(self.scrollable_frame, text="Стержень 1")
        a.grid(row=2, column=0, padx=5, pady=5)
        a.configure(bg="#76d5f5")

        temp_row = []
        temp_row.append(a)

        for i in range(7):
            entry = tk.Entry(self.scrollable_frame, width=10)
            entry.grid(row=2, column=i + 1, padx=5, pady=5)
            temp_row.append(entry)
            if i in (0, 5, 6):
                entry.insert(tk.END, "0")
                entry.config(validate='all', validatecommand=self.rn)
            else:
                entry.config(validate='all', validatecommand=self.rpn)


        self.fields.append(temp_row)

    def create_support_section(self):
        support_frame = tk.LabelFrame(self.root, text="Опоры", padx=5, pady=5)
        support_frame.place(relx=0.02, rely=0.32, relwidth=0.3, relheight=0.2)
        support_frame.configure(bg="#76d5f5")

        self.support_var = tk.StringVar(value="Правая")
        a = tk.Radiobutton(support_frame, text="Левая", variable=self.support_var, value="Левая")
        a.pack(anchor="w")
        a.configure(bg="#76d5f5", activebackground="#76d5f5")
        b = tk.Radiobutton(support_frame, text="Правая", variable=self.support_var, value="Правая")
        b.pack(anchor="w")
        b.configure(bg="#76d5f5", activebackground="#76d5f5")
        c = tk.Radiobutton(support_frame, text="Обе", variable=self.support_var, value="Обе")
        c.pack(anchor="w")
        c.configure(bg="#76d5f5", activebackground="#76d5f5")

    def create_file_section(self):
        file_frame = tk.LabelFrame(self.root, text="Файл", padx=5, pady=5)
        file_frame.place(relx=0.35, rely=0.32, relwidth=0.3, relheight=0.2)
        file_frame.configure(bg="#76d5f5")

        load_button = tk.Button(file_frame, text="Открыть", command=self.open_f, width=10)
        load_button.pack(pady=10)
        load_button.configure(bg="#20bff5", activebackground="#76d5f5")

        save_button = tk.Button(file_frame, text="Сохранить", command=self.save_f, width=10)
        save_button.pack(pady=10)
        save_button.configure(bg="#20bff5", activebackground="#76d5f5")

    def create_calculation_section(self):
        calc_frame = tk.LabelFrame(self.root, text="Расчет", padx=5, pady=5)
        calc_frame.place(relx=0.68, rely=0.32, relwidth=0.29, relheight=0.2)
        calc_frame.configure(bg="#76d5f5")

        full_button = tk.Button(calc_frame, text="Полный", width=10, command=self.full_calculation)
        full_button.pack(pady=10)
        full_button.configure(bg="#20bff5", activebackground="#76d5f5")

        section_button = tk.Button(calc_frame, text="Сечение", width=10, command=self.section_calculations)
        section_button.pack(pady=10)
        section_button.configure(bg="#20bff5", activebackground="#76d5f5")

    def create_construction_section(self):
        construction_frame = tk.LabelFrame(self.root, text="Конструкция", padx=5, pady=5)
        construction_frame.place(relx=0.02, rely=0.52, relwidth=0.95, relheight=0.45)
        construction_frame.configure(bg="#76d5f5")

        show_button = tk.Button(construction_frame, text="Отобразить", command=self.visualize)
        show_button.place(relx=0.02, rely=0.02)
        show_button.configure(bg="#20bff5", activebackground="#76d5f5")

        self.visual_field = tk.Canvas(construction_frame, bg="#a5e5fa")
        self.visual_field.place(relx=0.15, rely=0.02, relwidth=0.85, relheight=0.99)


    def add_steel(self):
        idx = len(self.fields)

        l = tk.Label(self.scrollable_frame, text=f"Стержень {idx+1}")
        l.grid(row=idx+2, column=0, padx=5, pady=5)
        l.configure(bg="#76d5f5")

        temp_row = [l]
        for i in range(6):
            e = tk.Entry(self.scrollable_frame, width=10)
            e.grid(row=idx+2, column=i+2, padx=5, pady=5)
            temp_row.append(e)
            if i in (4, 5):
                e.insert(tk.END, "0")
                e.config(validate='all', validatecommand=self.rn)
            else:
                e.config(validate='all', validatecommand=self.rpn)

        b = tk.Button(self.scrollable_frame, text='Убрать', command=lambda: self.delete_steel(temp_row))
        b.grid(row=idx + 2, column=1, padx=5, pady=5)
        b.configure(bg="#20bff5", activebackground="#76d5f5")
        temp_row.append(b)

        self.fields.append(temp_row)

        self.update_steel()


    def update_steel(self):
        for idx, row in enumerate(self.fields, start=1):
            label = row[0]
            label.config(text=f"Стержень {idx}")

            for widget in row:
                widget.grid_configure(row=idx+1)


    def delete_steel(self, row):
        for w in row:
            w.grid_remove()

        self.fields.remove(row)
        self.update_steel()

    def clear_all(self):
        for w in self.fields[1:]:
            self.delete_steel(w)
        for i, e in enumerate(self.fields[0][1:]):
            e.delete(0, tk.END)
            if i in (0, 5, 6):
                e.insert(0, '0')

    def clear_all_for_f(self):
        for w in self.fields[1:]:
            self.delete_steel(w)
        for i, e in enumerate(self.fields[0][1:]):
            e.delete(0, tk.END)

    def get_input(self):
        self.input_data.clear()

        data = self.input_data

        for i, row in enumerate(self.fields):
            if i == 0:
                data['f_start'].append(row[1].get())
                data['S'].append(row[2].get())
                data['L'].append(row[3].get())
                data['E'].append(row[4].get())
                data['max_f'].append(row[5].get())
                data['q'].append(row[6].get())
                data['f'].append(row[7].get())
            else:
                data['S'].append(row[1].get())
                data['L'].append(row[2].get())
                data['E'].append(row[3].get())
                data['max_f'].append(row[4].get())
                data['q'].append(row[5].get())
                data['f'].append(row[6].get())

        block_map = {
            "Левая": 1,
            "Правая": 2,
            "Обе": 3
        }
        block = self.support_var.get()

        data['block'] = block_map[block]

    def save_f(self):
        self.get_input()
        data = self.input_data
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)


    def open_f(self):
        self.clear_all_for_f()

        file_path = filedialog.askopenfilename(defaultextension=".json",
                                               filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                self.fields[0][1].insert(0, data['f_start'])
                self.fields[0][2].insert(0, data['S'][0])
                self.fields[0][3].insert(0, data['L'][0])
                self.fields[0][4].insert(0, data['E'][0])
                self.fields[0][5].insert(0, data['max_f'][0])
                self.fields[0][6].insert(0, data['q'][0])
                self.fields[0][7].insert(0, data['f'][0])

                for row in zip(data['S'][1:], data['L'][1:], data['E'][1:], data['max_f'][1:], data['q'][1:], data['f'][1:]):
                    self.add_steel()
                    for i, val in enumerate(row, start=1):
                        if i in (0, 5, 6):
                            self.fields[-1][i].delete(0, tk.END)
                        self.fields[-1][i].insert(0, val)

                block_map = {
                    1: "Левая",
                    2: "Правая",
                    3: "Обе"
                }
                block = block_map[data['block']]
                self.support_var.set(block)

                self.visualize()

    def visualize(self):
        self.get_input()
        if Checks.mom_check(self.input_data):
            self.input_data["L"] = Visual.prepare_data(self.input_data["L"], 10)
            ls = [float(val) for val in self.input_data["L"]]

            hs = [float(val) for val in self.input_data['S']]
            hs = Visual.prepare_data(hs, 10)

            conc_loads = [float(self.input_data["f_start"][0])]

            for val in self.input_data["f"]:
                conc_loads.append(float(val))

            dist_loads = self.input_data["q"]

            Visual.display_scheme(self.visual_field, ls, hs, conc_loads, dist_loads, self.input_data['block'])


    def full_calculation(self):
        self.get_input()

        if Checks.mom_check(self.input_data):
            all_calcs = MainCalc.TABLES_DATA(self.input_data, 5)
            MainCalc.TABLES(all_calcs)


    def section_calculations(self):
        self.get_input()

        if Checks.mom_check(self.input_data):
            SectionCalc.show_section_window(self.input_data)
