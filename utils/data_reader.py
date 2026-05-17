import openpyxl
import csv
import json
import os


def data_reader(file_name, sheet_name=None):

    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_dir, file_name)

    extension = os.path.splitext(file_path)[1]

    data = []

    if extension == ".xlsx":

        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook[sheet_name]

        for row in sheet.iter_rows(min_row=2, values_only=True):

            cleaned_row = []

            for cell in row:
                cleaned_row.append("" if cell is None else str(cell))

            data.append(cleaned_row)

    elif extension == ".csv":

        with open(file_path, newline='', encoding='utf-8') as file:

            reader = csv.reader(file)

            next(reader)  # bỏ header

            for row in reader:

                cleaned_row = []

                for cell in row:
                    cleaned_row.append("" if cell is None else str(cell))

                data.append(cleaned_row)
    elif extension == ".json":

        with open(file_path, encoding='utf-8') as file:

            json_data = json.load(file)

            for item in json_data:

                cleaned_row = []

                for value in item.values():
                    cleaned_row.append("" if value is None else str(value))

                data.append(cleaned_row)

    else:
        raise ValueError(f"Unsupported file type: {extension}")

    return data