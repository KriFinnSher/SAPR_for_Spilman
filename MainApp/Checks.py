import re
from tkinter import messagebox


def mom_check(data):
    for key, values in list(data.items())[:-1]:
        if any(val == '' for val in values):
            messagebox.showerror('Ошибка', 'Пожалуйста, заполните все поля ввода')
            return False

    e, s, l = data['E'], data['S'], data['L']

    for eal in zip(e, s, l):
        if float(eal[0]) * float(eal[1]) * float(eal[2]) == 0:
            messagebox.showerror('Ошибка', 'Все поля из [E, A, L] должны иметь ненулевое значение')
            return False

    return True

def check_1(val):
    pattern = r'^([1-9]\d*|)$'
    return re.match(pattern, val) is not None


def check_2(val):
    pattern = r'^(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None


def check_3(val):
    pattern = r'^-?(0(\.\d*)?|[1-9]\d*(\.\d*)?)?$'
    return re.match(pattern, val) is not None