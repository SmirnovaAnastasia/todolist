from datetime import datetime
import tkinter as tk
from tkinter import ttk
from Function.interface import StartPage, DayList, NotDone, Archive, AddNewDoing
from Function.database import overwrite_from_all_rows, get_all_tasks


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("1000x600")


        # creating a container
        container = tk.Frame(self, width=100, height=100)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, DayList, NotDone, Archive, AddNewDoing):
            frame = F(container, self)

            # initializing frame of that object from
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        self.frames[page_name].tkraise()  # Показываем страницу

    def reset_frame(self, target_frame_class):
        """
        Пересоздает указанный фрейм и показывает его
        """
        # Получаем container из любого существующего фрейма
        container = None
        for frame in self.frames.values():
            container = frame.master
            break

        if container:
            # Уничтожаем старый фрейм
            if target_frame_class in self.frames:
                old_frame = self.frames[target_frame_class]
                old_frame.destroy()

            # Создаем новый фрейм
            new_frame = target_frame_class(container, self)
            self.frames[target_frame_class] = new_frame
            new_frame.grid(row=0, column=0, sticky="nsew")

            # Показываем новый фрейм
            self.show_frame(target_frame_class)

app = tkinterApp()
app.mainloop()


