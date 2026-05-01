import openpyxl
from openpyxl.styles import Font, Alignment
import os

def write_test_results_excel(results, filename="test_results.xlsx", sheet_name="Test Results"):
    if not os.path.exists(filename):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = sheet_name
        ws.append([
            "Time", "Test Name", "Keyword/Email", "Password",
            "Expected", "Actual", "Status", "Screenshot"
        ])

        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")

        wb.save(filename)

    wb = openpyxl.load_workbook(filename)
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
    else:
        ws = wb.create_sheet(sheet_name)
        ws.append([
            "Time", "Test Name", "Keyword/Email", "Password",
            "Expected", "Actual", "Status", "Screenshot"
        ])
    for result in results:
        ws.append([
            result.get("Time", ""),
            result.get("Test Name", ""),
            result.get("Email", result.get("Keyword", "")),
            result.get("Password", result.get("Keyword", "")),
            result.get("Expected", ""),
            result.get("Actual", ""),
            result.get("Status", ""),
            result.get("Screenshot", "")
        ])

    wb.save(filename)
