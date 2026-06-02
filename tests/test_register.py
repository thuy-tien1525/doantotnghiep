import os
import pytest
from utils.data_reader import data_reader
from pages.register_page import RegisterPage
from utils.test_result_writer_excel import write_test_results_excel
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait


test_data = data_reader("Data/register_data.csv", "register_data")
all_results = []


@pytest.mark.parametrize(
    "index,first_name,last_name,email,phone,password,expected_result",
    [
        (i + 1, *row)
        for i, row in enumerate(test_data)
    ]
)
def test_registration(
        browser,
        index,
        first_name,
        last_name,
        email,
        phone,
        password,
        expected_result
):

    driver = browser
    reg_page = RegisterPage(driver)

    driver.get("https://thienlong.vn/account/register")

    test_name = f"test_registration_{index}"

    screenshot_path = ""
    actual_result = ""
    status = "FAIL"

    try:

        reg_page.register(
            first_name,
            last_name,
            email,
            phone,
            password
        )

        # =========================
        # FIX: wait + no params
        # =========================
        actual_result = WebDriverWait(driver, 10).until(
            lambda d: reg_page.get_message()
        ).strip()

        if expected_result.strip().lower() in actual_result.lower():
            status = "PASS"
        else:
            raise AssertionError(
                f"Expected: {expected_result}, Actual: {actual_result}"
            )

    except Exception as e:

        screenshot_dir = "report/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)

        screenshot_path = os.path.join(
            screenshot_dir,
            f"{test_name}.png"
        )

        driver.save_screenshot(screenshot_path)

        if not actual_result:
            actual_result = f"NO MESSAGE - {str(e)}"

    all_results.append({

        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "Test Name": test_name,
        "First Name": first_name,
        "Last Name": last_name,
        "Email": email,
        "Phone": phone,
        "Password": password,

        "Expected": expected_result,
        "Actual": actual_result,
        "Status": status,

        "Screenshot": screenshot_path if status == "FAIL" else ""

    })

    assert status == "PASS", (
        f"[{test_name}] "
        f"Expected: {expected_result}, "
        f"Actual: {actual_result}"
    )


def teardown_module(module):

    filename = "report/test_results_register.xlsx"

    write_test_results_excel(
        all_results,
        filename=filename,
        sheet_name="Test Results Register"
    )