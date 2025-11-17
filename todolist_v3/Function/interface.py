import tkinter as tk
from tkinter import ttk
from datetime import datetime

from dns.name import empty

from Function.database import overwrite_from_all_rows, get_all_tasks
# from  functions import *

LARGEFONT = ("Verdana", 15, "bold")
now = datetime.now().strftime("%Y.%m.%d")

all_tasks = get_all_tasks()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.configure(background='#7fb5b5')

        label = ttk.Label(self, text=f'Здравствуй! Сегодня {str(now[8:]) + str(now[4:8]) + str(now[:4])}. Что вы хотите сделать?', font=LARGEFONT, background='#7fb5b5', foreground='#366161')

        label.grid(row=0, column=0, padx=205, pady=60)

        style = ttk.Style()
        style.configure("Large.TButton",
                        padding=(0, 5),  # (padx, pady)
                        width=50,
                        font=('Verdana', 14),
                        bg= "#4a8282",
                        foreground="#4a8282")

        button1 = ttk.Button(self, text="Список дня",
                             command=lambda: controller.reset_frame(DayList), style="Large.TButton")


        button1.grid(row=2, column=0, padx=90, pady=20)

        button2 = ttk.Button(self, text="Невыполненные",
                             command=lambda: controller.reset_frame(NotDone), style="Large.TButton")

        button2.grid(row=4, column=0, padx=30, pady=20)

        button3 = ttk.Button(self, text="Архив",
                             command=lambda: controller.reset_frame(Archive), style="Large.TButton")

        button3.grid(row=6, column=0, padx=30, pady=20)



# second window frame page1
class DayList(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background='#7fb5b5')
        self.setup_table()

        style = ttk.Style()
        style.configure("Back.TButton",
                        padding=(0, 5),  # (padx, pady)
                        width=10,
                        font=('Verdana', 12),
                        bg="#4a8282",
                        foreground="#4a8282")

        style = ttk.Style()
        style.configure("Add.TButton",
                        padding=(0, 5),  # (padx, pady)
                        width=25,
                        font=('Verdana', 12),
                        bg="#4a8282",
                        foreground="#4a8282")

        button0 = ttk.Button(self, text="Добавить запись",
                             command=lambda: controller.reset_frame(AddNewDoing), style="Add.TButton")

        button1 = ttk.Button(self, text="Назад",
                             command=lambda: controller.reset_frame(StartPage), style="Back.TButton")

        button0.grid(row=2, column=0, padx=10, pady=10)
        button1.grid(row=3, column=0, padx=10, pady=10)

    def setup_table(self):
        # Фрейм таблицы
        # Заголовок таблицы
        table_title = ttk.Label(self,
                                     text="Дела на день",
                                     font=("Verdana", 14, "bold"), background='#7fb5b5', foreground='#366161')
        table_title.grid(row=0, column=0, padx=220, pady=40)


        # Создаем таблицу
        self.create_table()

    def create_table(self):
        # Treeview
        data_table = ttk.Treeview(self,
                                       columns=("col1", "col2", "col3"),
                                       show="headings",
                                       height=5)

        data_table.heading("col1", text="+")
        data_table.heading("col2", text="Дело")
        data_table.heading("col3", text="Нужность")

        data_table.column("col1", width=30)
        data_table.column("col2", width=600)
        data_table.column("col3", width=310)

        # Style for treeview
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)

        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="#4a8282", font=("Verdana", 10, "bold"))

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=data_table.yview)
        data_table.configure(yscrollcommand=scrollbar.set)

        data_table.grid(row=1, column=0, padx=10, pady=10)
        scrollbar.grid(row=1, column=4, padx=10, pady=10)


        here = 1

        for i in all_tasks:
            if str(i[0]) == now:
                # print('find!')
                here = 0

        if here == 1:
            new_part = (now, [])

            all_tasks.append(new_part)
            overwrite_from_all_rows(all_tasks)


        for row in all_tasks:
            if str(row[0]) == now:

                str_ = ' ' * 90 + row[0][8:] + row[0][4:8] + row[0][:4]
                data_table.insert("", "end", values=('', str_, ''))
                for row1 in row[1]:

                    need = ''
                    if row1[2] is True:
                        need = '[Нужно]'
                    else:
                        need = '[Не нужно]'
                    #
                    # combo = ttk.Combobox(self)
                    # combo['values'] = ('[Нужно]', '[Не нужно]')
                    # combo.current(0)  # установите вариант по умолчанию
                    # combo.grid(column=0, row=0)


                    if row1[1] is True:
                        status = '[+]'
                    else:
                        status = '[-]'
                    data_table.insert("", "end", values=(status, row1[0], need))


# third window frame page2
class NotDone(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background='#7fb5b5')
        self.setup_table()

        # button to show frame 3 with text
        style = ttk.Style()
        style.configure("Back.TButton",
                        padding=(0, 5),  # (padx, pady)
                        width=10,
                        font=('Verdana', 12),
                        bg="#4a8282",
                        foreground="#4a8282")
        # layout3
        button1 = ttk.Button(self, text="Назад",
                             command=lambda: controller.reset_frame(StartPage), style="Back.TButton")

        button1.grid(row=2, column=0, padx=10, pady=10)

    def setup_table(self):
        table_title = ttk.Label(self,
                                text="Невыполненные дела",
                                font=("Verdana", 14, "bold"), background='#7fb5b5', foreground='#366161')
        table_title.grid(row=0, column=0, padx=220, pady=40)

        # Создаем таблицу
        self.create_table()

    def create_table(self):
        # Treeview как атрибут класса для доступа из других методов
        data_table = ttk.Treeview(self,
                                  columns=("col1", "col2", "col3"),
                                  show="headings",
                                  height=5)

        data_table.heading("col1", text="+")
        data_table.heading("col2", text="Дело")
        data_table.heading("col3", text="Нужность")

        data_table.column("col1", width=30)
        data_table.column("col2", width=600)
        data_table.column("col3", width=310)

        style = ttk.Style()
        style.configure('Treeview', rowheight=30)

        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="#4a8282", font=("Verdana", 10, "bold"))

        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=data_table.yview)
        data_table.configure(yscrollcommand=scrollbar.set)

        data_table.grid(row=1, column=0, padx=10, pady=10)
        scrollbar.grid(row=1, column=4, padx=10, pady=10)


        for row in all_tasks:
            str_ = ' ' * 90 + row[0][8:] + row[0][4:8] + row[0][:4]
            data_table.insert("", "end", values=('', str_, ''))
            for row1 in row[1]:
                if row1[1] is False:
                    if row1[2] is True:
                        need = '[Нужно]'
                    else:
                        need = '[Не нужно]'

                    if row1[1] is True:
                        status = '[+]'
                    else:
                        status = '[-]'
                    data_table.insert("", "end", values=(status, row1[0], need))

            data_table.insert("", "end", values=('', '', ''))

# third window frame page2
class Archive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background='#7fb5b5')
        self.setup_table()

        style = ttk.Style()
        style.configure("Back.TButton",
                        padding=(0, 5),  # (padx, pady)
                        width=10,
                        font=('Verdana', 12),
                        bg="#4a8282",
                        foreground="#4a8282")

        button1 = ttk.Button(self, text="Назад",
                             command=lambda:  controller.reset_frame(StartPage), style="Back.TButton")

        button1.grid(row=2, column=0, padx=10, pady=10)

    def setup_table(self):
        # Фрейм таблицы
        # Заголовок таблицы
        table_title = ttk.Label(self,
                                text="Архив",
                                font=("Verdana", 14, "bold"), background='#7fb5b5', foreground='#366161')
        table_title.grid(row=0, column=0, padx=220, pady=40)

        # Создаем таблицу
        self.create_table()

    def create_table(self):
        # Treeview как атрибут класса для доступа из других методов
        data_table = ttk.Treeview(self,
                                  columns=("col1", "col2", "col3"),
                                  show="headings",
                                  height=5)
        data_table.heading("col1", text="+")
        data_table.heading("col2", text="Дело")
        data_table.heading("col3", text="Нужность")

        data_table.column("col1", width=30)
        data_table.column("col2", width=600)
        data_table.column("col3", width=310)

        style = ttk.Style()
        style.configure('Treeview', rowheight=30, foreground="#4a8282")

        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="#4a8282", font=("Verdana", 10, "bold"))

        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=data_table.yview)
        data_table.configure(yscrollcommand=scrollbar.set)

        data_table.grid(row=1, column=0, padx=10, pady=10)
        scrollbar.grid(row=1, column=4, padx=10, pady=10)

        for row in all_tasks:
            if str(row[0]) != now:
                str_ = ' ' * 90 + row[0][8:] + row[0][4:8] + row[0][:4]
                data_table.insert("", "end", values=('', str_, ''))
                for row1 in row[1]:
                    if row1[2] is True:
                        need = '[Нужно]'
                    else:
                        need = '[Не нужно]'

                    if row1[1] is True:
                        status = '[+]'
                    else:
                        status = '[-]'
                    data_table.insert("", "end", values=(status, row1[0], need))

                data_table.insert("", "end", values=('', '', ''))

class AddNewDoing(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def ClickFunction():
            res = "[Добавлена запись '{}']".format(txt.get())
            lbl2.configure(text=res)

            str_ = txt.get()
            print(str_)

            txt.delete(0, tk.END)

            for i in range(len(all_tasks)):
                if str(all_tasks[i][0]) == now:
                    new_doing = [str_, False, True]
                    all_tasks[i][1].append(new_doing)

            overwrite_from_all_rows(all_tasks)

        self.configure(background='#7fb5b5')

        lbl = ttk.Label(self, text="Введите новое дело:",  font=("Verdana", 14, "bold"), background='#7fb5b5', foreground="#4a8282")
        lbl.grid(column=0, row=1, padx=300, pady=10)

        txt = ttk.Entry(self, width=30, font=("Verdana", 12), foreground='#366161')
        txt.grid(column=0, row=2, padx=300, pady=10)

        style = ttk.Style()
        style.configure("AddNew.TButton",
                        padding=(0, 5),  # (padx, pady)
                        width=10,
                        font=('Verdana', 12),
                        bg="#4a8282",
                        foreground="#4a8282")

        btn = ttk.Button(self, text="Добавить", command=ClickFunction, style="AddNew.TButton")
        btn.grid(column=0, row=3, padx=300, pady=10)

        style = ttk.Style()
        style.configure("Back.TButton",
                        padding=(0, 5),  # (padx, pady)
                        width=10,
                        font=('Verdana', 12),
                        bg="#4a8282",
                        foreground="#4a8282")

        button1 = ttk.Button(self, text="Назад",
                             command=lambda: controller.reset_frame(DayList), style="Back.TButton")

        button1.grid(column=0, row=4, padx=300, pady=10)

        lbl2 = ttk.Label(self, text="", font=("Verdana", 14, "bold"), background='#7fb5b5',
                        foreground="#4a8282")
        lbl2.grid(column=0, row=5, padx=0, pady=10)
