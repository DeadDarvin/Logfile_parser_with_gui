from tkinter import *
from tkinter import filedialog
from parser_logfile.excel_writer import writer
from tkinter.messagebox import showerror, showinfo
import re
import os


class Root(Tk):
    """ Класс окна программы"""
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.input_file_entry = Entry()
        self.output_dir_entry = Entry()

    @staticmethod
    def write_choice_path_in_graph_str(file, directory):
        """
        Записывает в граф.строку
        выбранный через кнопку
        путь файла или каталога
        """
        if directory:
            filepath = filedialog.askdirectory()
        else:
            filepath = filedialog.askopenfilename()

        file.insert(0, filepath)

    @staticmethod
    def check_valid(text, input_file=False, output_dir=False):
        """
        Проверяет корректность заданных путей и имени входного файла.
        Возвращает False, если хотя бы одно условие не выполняется.
        """
        if text == "":
            return False

        if input_file:
            if not os.path.isfile(text):
                return False
            file_name = text.split("/")[-1]
            pattern = r"\b.*[.]log"
            if not re.match(pattern, file_name):
                return False

        if output_dir:
            if not os.path.isdir(text):
                return False

        return True

    def create_text(self, text, **kwargs):
        text_label = Label(
            self,
            text=text,
            **kwargs,
        )
        return text_label

    def create_button(self, text, format_file_name, directory=False):
        """
        text - текст на кнопке
        format_file_name - имя экземпляра Entry
        directory - если True, будет выбор каталога на уровне TK
        """
        btn = Button(
            self,
            text=text,
            command=lambda: self.write_choice_path_in_graph_str(format_file_name, directory),
        )
        return btn

    def create_gen_button(self, text):
        btn = Button(
            self,
            text=text,
            command=self.start,
        )
        return btn

    def start(self):
        """
        Основная функция.
        Создаёт и наполняет словарь с путями файлов.
        Передаёт словарь для парсинга.
        """
        paths_dict = {}
        flag = True

        input_file = self.input_file_entry.get()
        if self.check_valid(input_file, input_file=True):
            paths_dict['input_file'] = input_file
        else:
            flag = False
            showerror('Ошибка!', 'Некорректное имя входного файла')
            self.input_file_entry.delete(0, END)

        output_dir = self.output_dir_entry.get()
        if self.check_valid(output_dir, output_dir=True):
            paths_dict['output_dir'] = output_dir
        else:
            flag = False
            showerror('Ошибка!', 'Некорректное имя выходной папки')
            self.output_dir_entry.delete(0, END)

        if flag:
            is_done = writer(paths_dict)

            if is_done:
                showinfo('Готово!', 'Работа успешно завершена.')
            else:
                showerror('Ошибка!', 'Некорректные данные или конченная программа')
            self.destroy()


def main():
    # Создание окна
    root = Root()
    root.title('Ваш парсер')
    root.geometry('400x400')
    root.resizable(width=False, height=False)
    root.config(bg='grey')

    # Создание и позиционирование элементов
    text1 = root.create_text(
        text='Укажите путь входного файла:',
        bg='grey',
        font=('Arial', 12, 'bold')
    )
    text1.pack(pady=10)

    root.input_file_entry.place(height=30, width=280, anchor=NW, x=10, y=50)

    btn1 = root.create_button('Выбрать', format_file_name=root.input_file_entry)
    btn1.place(height=30, width=80, x=305, y=50)

    text2 = root.create_text(
        text='Укажите путь для результата:',
        bg='grey',
        font=('Arial', 12, 'bold')
    )
    text2.pack(pady=70)

    root.output_dir_entry.place(height=30, width=280, anchor=NW, x=10, y=150)

    btn2 = root.create_button('Выбрать', format_file_name=root.output_dir_entry, directory=True)
    btn2.place(height=30, width=80, x=305, y=150)

    gen_btn = root.create_gen_button('Старт')
    gen_btn.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
