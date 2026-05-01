import openpyxl
import os

def read_excel_data(file_name, sheet_name):
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_dir, file_name)

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        cleaned_row = []
        for cell in row:
            if cell is None:
                cleaned_row.append("")
            else:
                cleaned_row.append(str(cell))
        data.append(cleaned_row)

    return data
