import xlsxwriter
from datetime import date
from parser_logfile.parser_bones import create_table_mass
from xlsxwriter.exceptions import FileCreateError


def writer(paths_dict):

    table_mass = create_table_mass(paths_dict['input_file'])  # Запуск парсинга

    try:
        column_names = list(table_mass[0].keys())  # Список ключей
    except IndexError:  # Возникновение исключения - ошибка в парсинге
        return False

    current_date = date.today()
    xlsxname = f'pars_{current_date}.xlsx'
    workbook = xlsxwriter.Workbook(f"{paths_dict['output_dir']}/{xlsxname}")

    worksheet = workbook.add_worksheet()
    worksheet.set_column(1, len(column_names), width=10)
    bold = workbook.add_format({'bold': True})  # Выделение жирным

    # Запись наименований
    row = col = 0
    for name in column_names:
        worksheet.write(row, col, name, bold)
        col += 1

    # Запись значений
    row = 1
    col = 0
    for row_dict in table_mass:
        for name in column_names:
            worksheet.write(row, col, row_dict[name])
            col += 1
        row += 1

    try:
        workbook.close()
    except FileCreateError:
        return False

    return True
