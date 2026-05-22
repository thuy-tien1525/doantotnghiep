import os
import pytest
from datetime import datetime
from utils.data_reader import data_reader
from utils.test_result_writer_excel import write_test_results_excel
from pages2.cart_page2 import CartPage
from pages2.Order_page2 import OrderPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
test_data = data_reader("Data/Order2_data.xlsx", "Order2_data")
all_results = []

@pytest.mark.parametrize(
    "index,fullname,email,phone,address,province,district,ward,expected_result",
    [(i + 1, *row) for i, row in enumerate(test_data)]
)
def   test_order2(browser, index, fullname, email, phone, address, province, district, ward, expected_result):
    driver = browser
    cart_page2 = CartPage(driver)
    order_page2 = OrderPage(driver)

    driver.maximize_window()
    driver.get("https://savani.vn/products/ao-thun-ngan-tay-co-tron-nam-mtsa502s6")

    test_name = f"test_order_{index}"
    screenshot_path = ""
    actual_result = ""
    status = "FAIL"

    try:

        order_page2.click_add_to_cart()
        cart_page2.click_checkout_popup()
        order_page2.click_checkout()
        order_page2.fill_customer_info(fullname, email, phone, address)
        order_page2.select_province(province)
        order_page2.select_district(district)
        order_page2.select_ward(ward)
        order_page2.click_continue()
        time.sleep(5)
        order_page2.click_complete_order_btn()

        try:
            WebDriverWait(driver, 10).until(
                lambda d: len(order_page2.get_message_text()) > 0
                          or order_page2.get_success_message() != ""
            )
        except TimeoutException:
            pass

        time.sleep(3)
        errors = []
        try:
            errors = order_page2.get_message_text()
        except Exception:
            try:
                time.sleep(2)
                errors = order_page2.get_message_text()
            except:
                errors = []
        if errors:
            actual_result = errors[0]  # lấy lỗi đầu tiên
        else:
            # Nếu không có lỗi, kiểm tra thông báo đặt hàng thành công
            actual_result = order_page2.get_success_message()
            if not actual_result:
                actual_result = ""

        status = "FAIL"
        try:
            if expected_result.strip() in actual_result.strip():
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
        "Full Name": fullname,
        "Email": email,
        "Phone": phone,
        "Address": address,
        "Province": province,
        "District": district,
        "Ward": ward,
        "Expected": expected_result,
        "Actual": actual_result,
        "Status": status,
        "Screenshot": screenshot_path if status == "FAIL" else ""
    })

    assert status == "PASS", f"[{test_name}] Expected: {expected_result}, Actual: {actual_result}"


def teardown_module(module):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report/test_results_order_{timestamp}.xlsx"
    write_test_results_excel(
        all_results,
        filename=filename,
        sheet_name="Test Results Order"
    )
