import pytest
import os

from utils.excel_reader import read_excel_data
from pages.register_page import RegisterPage

test_data = read_excel_data("Data/register_data.xlsx", "register_data")

@pytest.mark.parametrize("index,first_name,last_name,email,phone,password,expected_result", [
    (i + 1, *row) for i, row in enumerate(test_data)
])
def test_registration(browser, index, first_name, last_name, email, phone, password, expected_result, request):
    driver = browser
    reg_page = RegisterPage(driver)

    driver.get("https://thienlong.vn/account/register")

    reg_page.register(first_name, last_name, email, phone, password)

    actual_result = reg_page.get_message(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        password=password
    ).strip()

    test_name = f"test_registration_{index}"

    if actual_result != expected_result.strip():
        screenshot_dir = "report/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)

        pytest.fail(
            f"[{test_name}] Expected: {expected_result}, Actual: {actual_result}"
        )
