import time
import os
import pytest
from pages.login_page import LoginPage
from utils.excel_reader import read_excel_data
from utils.test_result_writer_excel import write_test_results_excel
from datetime import datetime


test_data = read_excel_data("Data/Login_data.xlsx", "login_data")
all_results = []

@pytest.mark.parametrize("index,email,password,expected_result", [
    (i + 1, *row) for i, row in enumerate(test_data)
])
def test_login(browser, index, email, password, expected_result):
    driver = browser
    login_page = LoginPage(driver)

    driver.get("https://thienlong.vn/")
    login_page.open_login_form()
    login_page.login(email, password)

    time.sleep(2)

    test_name = f"test_login_{index}"
    screenshot_path = ""
    actual_result = ""
    status = "FAIL"
    try:
        actual_result = login_page.get_error_message(email, password).strip()
        if actual_result == expected_result.strip():
            status = "PASS"
        else:
            raise AssertionError(f"Expected: {expected_result}, Actual: {actual_result}")
    except Exception as e:
        screenshot_dir = "report/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)
        if not actual_result:
            actual_result = str(e)

    all_results.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Name": test_name,
        "Email": email,
        "Password": password,
        "Expected": expected_result,
        "Actual": actual_result,
        "Status": status,
        "Screenshot": screenshot_path if status == "FAIL" else ""
    })

    assert status == "PASS", f"[{test_name}] Expected: {expected_result}, Actual: {actual_result}"

def teardown_module(module):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report/test_results_login_{timestamp}.xlsx"
    write_test_results_excel(
        all_results,
        filename=filename,
        sheet_name="Test Results Login"
    )