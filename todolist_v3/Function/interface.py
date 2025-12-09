import tkinter as tk
from doctest import master
from tkinter import ttk
from tkinter import *
from tkinter.ttk import Checkbutton
from datetime import datetime

from dns.name import empty

from Function.database import overwrite_from_all_rows, get_all_tasks
# from  functions import *

LARGEFONT = ("Verdana", 15, "bold")
now = datetime.now().strftime("%Y.%m.%d")

# all_tasks = get_all_tasks()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.configure(background='#7fb5b5')

        label = ttk.Label(self, text=f'Здравствуйте! Сегодня {str(now[8:]) + str(now[4:8]) + str(now[:4])}. Что вы хотите сделать?', font=LARGEFONT, background='#7fb5b5', foreground='#366161')

        label.grid(row=0, column=0, padx=180, pady=60)

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
        self.all_tasks_daily = get_all_tasks()

        self.data_table = ttk.Treeview(self,
                                       columns=("col1", "col2", "col3"),
                                       show="headings",
                                       height=5)

        self.data_table.heading("col1", text="+")
        self.data_table.heading("col2", text="Дело")
        self.data_table.heading("col3", text="Нужность")

        self.data_table.column("col1", width=30)
        self.data_table.column("col2", width=600)
        self.data_table.column("col3", width=310)

        # Style for treeview
        style = ttk.Style()
        style.configure('Treeview', rowheight=30)

        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="#4a8282", font=("Verdana", 10, "bold"))

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=self.data_table.yview)
        self.data_table.configure(yscrollcommand=scrollbar.set)

        self.data_table.grid(row=1, column=0, padx=10, pady=10)
        scrollbar.grid(row=1, column=4, padx=10, pady=10)


        here = 1

        for i in  self.all_tasks_daily:
            if str(i[0]) == now:
                # print('find!')
                here = 0

        if here == 1:
            new_part = (now, [])

            self.all_tasks_daily.append(new_part)
            overwrite_from_all_rows( self.all_tasks_daily)

        for row in  self.all_tasks_daily:
            if str(row[0]) == now:

                str_ = ' ' * 90 + row[0][8:] + row[0][4:8] + row[0][:4]
                self.data_table.insert("", "end", values=('', str_, ''))
                for row1 in row[1]:

                    need = ''
                    if row1[2] is True:
                        need = '[Нужно]'
                    else:
                        need = '[Не нужно]'

                    # Создаем изображения для чекбоксов
                    self.checked_img = tk.PhotoImage(width=16, height=16)
                    self.unchecked_img = tk.PhotoImage(width=16, height=16)

                    # Простые чекбоксы (можно заменить на реальные изображения)
                    self.draw_checkbox(self.checked_img, True)
                    self.draw_checkbox(self.unchecked_img, False)

                    if row1[1] is True:
                        status = '[✓]'
                    else:
                        status = '[✗]'

                    image = self.checked_img if row1[1] else self.unchecked_img
                    self.data_table.insert("", "end",values=(status, row1[0], need))
                    # # Привязываем обработчик клика
                    # self.data_table.bind('<Button-1>', self.on_click)

        self.data_table.bind('<Button-1>', lambda event: self.on_click(event))



    def draw_checkbox(self, img, checked):
        # Здесь можно нарисовать чекбокс или загрузить изображения
        color = 'green' if checked else 'red'
        img.put(color, (4, 4, 12, 12))

    def on_click(self, event):
        region = self.data_table.identify_region(event.x, event.y)
        if region == "cell":
            column = self.data_table.identify_column(event.x)
            item = self.data_table.identify_row(event.y)

            values_up = list(self.data_table.item(item, 'values'))
            if values_up[0] != '[✓]' and values_up[0] != '[✗]':
                print("It's data")

            elif column == "#1":
                item_num = int(item[1:], 16)
                num = item_num - 2 # без заголовка и первой даты

                numx = 0
                numy = 0
                for i in range(len(self.all_tasks_daily)):
                    if str(self.all_tasks_daily[i][0]) == now:
                        for j in range(len(self.all_tasks_daily[i][1])):
                            if num == j:
                                numx = i
                                numy = j
                                if self.all_tasks_daily[i][1][j][1] is False:
                                    self.all_tasks_daily[i][1][j][1] = True
                                else:
                                    print(self.all_tasks_daily[i][1][j])
                                    self.all_tasks_daily[i][1][j][1] = False

                # print(self.all_tasks_daily)
                overwrite_from_all_rows(self.all_tasks_daily)

                new_state = self.all_tasks_daily[numx][1][numy][1]

                # Обновляем отображение
                values = list(self.data_table.item(item, 'values'))
                values[0] = '[✓]' if new_state else '[✗]'
                self.data_table.item(item, values=values)

                print(f"Item {item}: {'Checked' if new_state else 'Unchecked'}")

            elif column == "#3":
                item_num = int(item[1:], 16)
                num = item_num - 2  # без заголовка и первой даты

                numx = 0
                numy = 0
                for i in range(len(self.all_tasks_daily)):
                    if str(self.all_tasks_daily[i][0]) == now:
                        for j in range(len(self.all_tasks_daily[i][1])):
                            if num == j:
                                numx = i
                                numy = j
                                if self.all_tasks_daily[i][1][j][2] is False:
                                    self.all_tasks_daily[i][1][j][2] = True
                                else:
                                    print(self.all_tasks_daily[i][1][j])
                                    self.all_tasks_daily[i][1][j][2] = False

                # print(self.all_tasks_daily)
                overwrite_from_all_rows(self.all_tasks_daily)

                new_state = self.all_tasks_daily[numx][1][numy][2]

                # Обновляем отображение
                values = list(self.data_table.item(item, 'values'))
                values[2] = '[Нужно]' if new_state else '[Не нужно]'
                self.data_table.item(item, values=values)

                print(f"Item {item}: {'Checked' if new_state else 'Unchecked'}")



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
        self.all_tasks_not_done = get_all_tasks()
        # print(self.all_tasks_not_done)

        # Treeview как атрибут класса для доступа из других методов
        self.data_table = ttk.Treeview(self,
                                  columns=("col1", "col2", "col3"),
                                  show="headings",
                                  height=5)

        self.data_table.heading("col1", text="+")
        self.data_table.heading("col2", text="Дело")
        self.data_table.heading("col3", text="Нужность")

        self.data_table.column("col1", width=30)
        self.data_table.column("col2", width=600)
        self.data_table.column("col3", width=310)

        style = ttk.Style()
        style.configure('Treeview', rowheight=30)

        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="#4a8282", font=("Verdana", 10, "bold"))

        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=self.data_table.yview)
        self.data_table.configure(yscrollcommand=scrollbar.set)

        self.data_table.grid(row=1, column=0, padx=10, pady=10)
        scrollbar.grid(row=1, column=4, padx=10, pady=10)


        for row in self.all_tasks_not_done:

            str_ = ' ' * 90 + row[0][8:] + row[0][4:8] + row[0][:4]
            self.data_table.insert("", "end", values=('', str_, ''))
            for row1 in row[1]:
                if row1[1] is False:
                    need = ''
                    if row1[2] is True:
                        need = '[Нужно]'
                    else:
                        need = '[Не нужно]'

                    # Создаем изображения для чекбоксов
                    self.checked_img = tk.PhotoImage(width=16, height=16)
                    self.unchecked_img = tk.PhotoImage(width=16, height=16)

                    # Простые чекбоксы (можно заменить на реальные изображения)
                    self.draw_checkbox(self.checked_img, True)
                    self.draw_checkbox(self.unchecked_img, False)

                    if row1[1] is True:
                        status = '[✓]'
                    else:
                        status = '[✗]'
                    

                    image = self.checked_img if row1[1] else self.unchecked_img
                    self.data_table.insert("", "end", values=(status, row1[0], need))

        self.data_table.bind('<Button-1>', lambda event: self.on_click(event))

    def draw_checkbox(self, img, checked):
        # Здесь можно нарисовать чекбокс или загрузить изображения
        color = 'green' if checked else 'red'
        img.put(color, (4, 4, 12, 12))

    def on_click(self, event):
        region = self.data_table.identify_region(event.x, event.y)
        if region == "cell":
            column = self.data_table.identify_column(event.x)
            item = self.data_table.identify_row(event.y)

            values_up = list(self.data_table.item(item, 'values'))
            if values_up[0] != '[✓]' and values_up[0] != '[✗]':
                print("It's data")

            elif column == "#1":
                item_num = int(item[1:], 16)
                num = item_num - 1

                ch = 0
                numx= 0
                numy = 0
                all_done = False
                for i in range(len(self.all_tasks_not_done)):
                    if all_done is True:
                        break
                    ch += 1
                    for j in range(len(self.all_tasks_not_done[i][1])):
                        # print(self.all_tasks_not_done[i][1][j])
                        if self.all_tasks_not_done[i][1][j][1] is False:
                            print(f"I'm here: {self.all_tasks_not_done[i][1][j]}")
                            if num == ch:
                                print(f'ch {ch}: {self.all_tasks_not_done[i][1][j]}')
                                self.all_tasks_not_done[i][1][j][1] = True

                                numx = i
                                numy = j

                                all_done = True
                                break
                            ch = ch + 1

                print(self.all_tasks_not_done)
                overwrite_from_all_rows(self.all_tasks_not_done)

                self.data_table.delete(item)

                # num_columns = len(self.data_table.item(item, 'values'))
                # empty_values = [''] * num_columns  # Создаем список пустых строк для всех колонок
                # self.data_table.item(item, values=empty_values)

            elif column == "#3":
                item_num = int(item[1:], 16)
                num = item_num - 2

                ch = 0
                numx = 0
                numy = 0
                all_done = False
                for i in range(len(self.all_tasks_not_done)):
                    if all_done is True:
                        break
                    for j in range(len(self.all_tasks_not_done[i][1])):
                        if self.all_tasks_not_done[i][1][j][1] is False:
                            if num == ch:
                                print(self.all_tasks_not_done[i][1][j])
                                self.all_tasks_not_done[i][1][j][2] = True

                                numx = i
                                numy = j

                                all_done = True
                                break
                            ch = ch + 1
                    num -= 1

                print(self.all_tasks_not_done)
                overwrite_from_all_rows(self.all_tasks_not_done)

                new_state = self.all_tasks_not_done[numx][1][numy][2]

                # Обновляем отображение
                values = list(self.data_table.item(item, 'values'))
                values[2] = '[Нужно]' if new_state else '[Не нужно]'
                self.data_table.item(item, values=values)

                print(f"Item {item}: {'Checked' if new_state else 'Unchecked'}")


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
        self.all_tasks_arch = get_all_tasks()
        # Treeview как атрибут класса для доступа из других методов
        self.data_table = ttk.Treeview(self,
                                  columns=("col1", "col2", "col3"),
                                  show="headings",
                                  height=5)
        self.data_table.heading("col1", text="+")
        self.data_table.heading("col2", text="Дело")
        self.data_table.heading("col3", text="Нужность")

        self.data_table.column("col1", width=30)
        self.data_table.column("col2", width=600)
        self.data_table.column("col3", width=310)

        style = ttk.Style()
        style.configure('Treeview', rowheight=30, foreground="#4a8282")

        style = ttk.Style()
        style.configure("Treeview.Heading", foreground="#4a8282", font=("Verdana", 10, "bold"))

        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=self.data_table.yview)
        self.data_table.configure(yscrollcommand=scrollbar.set)

        self.data_table.grid(row=1, column=0, padx=10, pady=10)
        scrollbar.grid(row=1, column=4, padx=10, pady=10)

        for row in self.all_tasks_arch:

            if str(row[0]) != now:

                str_ = ' ' * 90 + row[0][8:] + row[0][4:8] + row[0][:4]
                self.data_table.insert("", "end", values=('', str_, ''))
                for row1 in row[1]:
                    need = ''
                    if row1[2] is True:
                        need = '[Нужно]'
                    else:
                        need = '[Не нужно]'

                    # Создаем изображения для чекбоксов
                    self.checked_img = tk.PhotoImage(width=16, height=16)
                    self.unchecked_img = tk.PhotoImage(width=16, height=16)

                    # Простые чекбоксы (можно заменить на реальные изображения)
                    self.draw_checkbox(self.checked_img, True)
                    self.draw_checkbox(self.unchecked_img, False)

                    if row1[1] is True:
                        status = '[✓]'
                    else:
                        status = '[✗]'

                    image = self.checked_img if row1[1] else self.unchecked_img
                    self.data_table.insert("", "end", values=(status, row1[0], need))

        self.data_table.bind('<Button-1>', lambda event: self.on_click(event))

    def draw_checkbox(self, img, checked):
        # Здесь можно нарисовать чекбокс или загрузить изображения
        color = 'green' if checked else 'red'
        img.put(color, (4, 4, 12, 12))

    def on_click(self, event):
        region = self.data_table.identify_region(event.x, event.y)
        if region == "cell":
            column = self.data_table.identify_column(event.x)
            item = self.data_table.identify_row(event.y)

            values_up = list(self.data_table.item(item, 'values'))
            if values_up[0] != '[✓]' and values_up[0] != '[✗]':
                print("It's data")

            elif column == "#1":
                item_num = int(item[1:], 16)
                num = item_num - 2

                value1 = ''
                if item:  # Проверяем, что строка найдена
                    # Способ 1 - через item()
                    values = self.data_table.item(item)['values']
                    if values and len(values) > 1:
                        value1 = values[1]  # Второй столбец

                ch = 0
                numx = 0
                numy = 0
                all_done = False
                for i in range(len(self.all_tasks_arch)):
                    if all_done is True:
                        break
                    for j in range(len(self.all_tasks_arch[i][1])):
                        if num == ch:
                            print(self.all_tasks_arch[i][1][j])
                            if self.all_tasks_arch[i][1][j][1] is False:
                                self.all_tasks_arch[i][1][j][1] = True
                            else:
                                self.all_tasks_arch[i][1][j][1] = False

                            print(self.all_tasks_arch[i][1][j])


                            numx = i
                            numy = j

                            all_done = True
                            break
                        ch = ch + 1
                    num -= 1

                overwrite_from_all_rows(self.all_tasks_arch)
                new_state = self.all_tasks_arch[numx][1][numy][1]

                # Обновляем отображение
                values = list(self.data_table.item(item, 'values'))
                values[0] = '[✓]' if new_state else '[✗]'
                self.data_table.item(item, values=values)

                print(f"Item {item}: {'Checked' if new_state else 'Unchecked'}")

            elif column == "#3":
                item_num = int(item[1:], 16)
                num = item_num - 2

                value1 = ''
                if item:  # Проверяем, что строка найдена
                    # Способ 1 - через item()
                    values = self.data_table.item(item)['values']
                    if values and len(values) > 1:
                        value1 = values[1]  # Второй столбец

                ch = 0
                numx = 0
                numy = 0
                all_done = False
                for i in range(len(self.all_tasks_arch)):
                    if all_done is True:
                        break
                    for j in range(len(self.all_tasks_arch[i][1])):
                        if num == ch:
                            print(self.all_tasks_arch[i][1][j])
                            if self.all_tasks_arch[i][1][j][2] is False:
                                self.all_tasks_arch[i][1][j][2] = True
                            else:
                                self.all_tasks_arch[i][1][j][2] = False

                            print(self.all_tasks_arch[i][1][j])

                            numx = i
                            numy = j

                            all_done = True
                            break
                        ch = ch + 1
                    num -= 1

                overwrite_from_all_rows(self.all_tasks_arch)

                new_state = self.all_tasks_arch[numx][1][numy][2]

                # Обновляем отображение
                values = list(self.data_table.item(item, 'values'))
                values[2] = '[Нужно]' if new_state else '[Не нужно]'
                self.data_table.item(item, values=values)

                print(f"Item {item}: {'Checked' if new_state else 'Unchecked'}")


class AddNewDoing(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def ClickFunction():

            self.all_tasks_add = get_all_tasks()
            res = "[Добавлена запись '{}']".format(txt.get())
            lbl2.configure(text=res)

            str_ = txt.get()
            print(str_)

            txt.delete(0, tk.END)

            for i in range(len(self.all_tasks_add)):
                if str(self.all_tasks_add[i][0]) == now:
                    new_doing = [str_, False, True]
                    self.all_tasks_add[i][1].append(new_doing)

            overwrite_from_all_rows(self.all_tasks_add)

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
