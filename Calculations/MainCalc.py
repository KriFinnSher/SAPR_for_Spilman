from collections import defaultdict
import numpy as np
import tkinter as tk
from tkinter import ttk


def B_MAT(fs, qs, ls, s):
    size = len(ls) + 2
    pl_new, ql_new = [0] * size, [0] * size
    for p in fs:
        pl_new[p] = fs[p]
    for steel_num in qs:
        ql_new[steel_num] += qs[steel_num] * ls[steel_num] / 2
        ql_new[steel_num + 1] += qs[steel_num] * ls[steel_num] / 2
    b_mat = [pl_new[i] + ql_new[i] for i in range(size)][1:]
    if s == 1 or s == 3:
        b_mat[0] = 0
    if s == 2 or s == 3:
        b_mat[-1] = 0
    return b_mat


def A_MAT(ks, s):
    size = len(ks) + 1
    a_mat = [[0] * size for _ in range(size)]
    for l in range(size - 1):
        for i in range(2):
            for j in range(2):
                a_mat[i + l][j + l] += ks[l][i][j]
    if s == 1 or s == 3:
        a_mat[0][0] = 1
        for i in range(1, size):
            a_mat[0][i] = 0
            a_mat[i][0] = 0
    if s == 2 or s == 3:
        a_mat[-1][-1] = 1
        for i in range(0, size-1):
            a_mat[-1][i] = 0
            a_mat[i][-1] = 0
    return a_mat


def DELTA_VECTOR(a_mat, b_mat):
    a_mat = np.array(a_mat)
    b_mat = np.array(b_mat)
    delta = np.linalg.solve(a_mat, b_mat)
    delta_rounded = np.round(delta, 4).tolist()
    return delta_rounded


def K_MATS(data):
    k_mats = []
    S = data['S']
    L = data['L']
    E = data['E']
    ls = defaultdict(float)
    es = defaultdict(float)
    ss = defaultdict(float)
    for i, steel in enumerate(zip(S, L, E)):
        ls[i + 1] = float(steel[1])
        es[i + 1] = float(steel[2])
        ss[i + 1] = float(steel[0])
    for k in range(1, len(data['f']) + 1):
        k_mat = [[es[k] * ss[k] / ls[k], -es[k] * ss[k] / ls[k]], [-es[k] * ss[k] / ls[k], es[k] * ss[k] / ls[k]]]
        k_mats.append(k_mat)
    return k_mats


def GET_DELTAS(data):
    f_start = data['f_start']
    fs = data['f']
    ls = data['L']
    q = data['q']
    lens = defaultdict(float)
    for i, l in enumerate(ls):
        lens[i+1] = float(l)
    qs = {i+1: float(val) for i, val in enumerate(q)}
    ps = defaultdict(float)
    ps[1] = float(f_start[0])
    for i in range(len(fs)):
        ps[i+2] += float(fs[i])
    b_mat = B_MAT(ps, qs, lens, data['block'])
    a_mat = A_MAT(K_MATS(data), data['block'])
    return DELTA_VECTOR(a_mat, b_mat)


def GET_SECTION(data, num, x_val):
    u0 = GET_DELTAS(data)[num - 1]
    ul = GET_DELTAS(data)[num]
    steel_len = float(data['L'][num - 1])
    steel_e = float(data['E'][num - 1])
    steel_a = float(data['S'][num - 1])
    steel_q = float(data['q'][num - 1])
    u_val = round(U_VAL(x_val, u0, ul, steel_len, steel_q, steel_e, steel_a), 4)
    n_val = round(N_VAL(x_val, u0, ul, steel_len, steel_q, steel_e, steel_a), 4)
    max_f_val = round(MAX_F_VAL(n_val, steel_a), 4)
    return u_val, n_val, max_f_val


def TABLES_DATA(data, d):
    size = len(data['f']) + 1
    tables = [[] for _ in range(size)]
    ss = data['S']
    ls = data['L']
    es = data['E']
    max_f = data['max_f']
    qs = data['q']
    us = GET_DELTAS(data)
    for i, bar in enumerate(zip(ss, ls, es, max_f, qs)):
        u0, ul = us[i], us[i + 1]
        for j in range(d + 1):
            x = round(float(bar[1]) / d * j, 4)
            n = N_VAL(x, u0, ul, float(bar[1]), float(bar[4]), float(bar[2]), float(bar[0]))
            u = U_VAL(x, u0, ul, float(bar[1]), float(bar[4]), float(bar[2]), float(bar[0]))
            s = MAX_F_VAL(n, float(bar[0]))
            tables[i+1].append((x, n, u, s, float(bar[3])))
    del tables[0]
    return tables


def TABLES(tables):
    root = tk.Tk()
    root.title("Таблицы расчетов")
    root.geometry('540x370')
    root.resizable(False, False)
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar_y = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar_y.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar_y.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.config(bg="#048dba")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    headers = ["x", "N(x)", "U(x)", "σ(x)", "[σ]"]

    for table_index, table in enumerate(tables):
        frame = tk.LabelFrame(scrollable_frame, text=f"Таблица {table_index + 1}")
        frame.pack(fill="x", padx=10, pady=5)
        frame.config(bg="#76d5f5")

        tree = ttk.Treeview(frame, columns=headers, show="headings", height=6)
        tree.pack(fill="x")

        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor="center", width=100)

        tree.tag_configure('alert', background='red')

        for row in table:
            if abs(float(row[-2])) > float(row[-1]):
                tree.insert('', 'end', values=row, tags='alert')
            else:
                tree.insert("", "end", values=row)


def U_VAL(x, u0, ul, l, q, e, a):
    return round(u0 + (x / l) * (ul - u0) + (q * l ** 2) / (2 * e * a) * (x / l) * (1 - x / l), 4)


def N_VAL(x, u0, ul, l, q, e, a):
    return round((e * a / l) * (ul - u0) + (q * l / 2) * (1 - 2 * x / l), 4)


def MAX_F_VAL(n, a):
    return round(n / a, 4)