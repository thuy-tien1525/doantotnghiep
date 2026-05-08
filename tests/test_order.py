import os
import time
import pytest
from datetime import datetime
from utils.excel_reader import read_excel_data
from utils.test_result_writer_excel import write_test_results_excel
from pages.cart_page import CartPage
from pages.Order_page import OrderPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

test_data = read_excel_data("Data/Order_data.xlsx", "Order_data")
all_results = []

@pytest.mark.parametrize(
    "index,fullname,email,phone,address,province,district,ward,expected_result",
    [(i + 1, *row) for i, row in enumerate(test_data)]
)
def   test_order(browser, index, fullname, email, phone, address, province, district, ward, expected_result):
    driver = browser
    cart_page = CartPage(driver)
    order_page = OrderPage(driver)

    driver.maximize_window()
    driver.get("https://thienlong.vn/collections/may-tinh-khoa-hoc-1?q=filter=((collectionid:product=1003213612))&page=1&sortby=manual&view=grid")

    test_name = f"test_order_{index}"
    screenshot_path = ""
    actual_result = ""
    status = "FAIL"

    try:
        cart_page.click_quick_view()
        product_name = cart_page.get_product_name()

        assert cart_page.select_color(), "Sản phẩm hết hàng"
        cart_page.click_add_to_cart()
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "swal-overlay"))
        )

        cart_page.open_cart()

        name_in_cart = cart_page.get_text_in_cart()

        assert product_name == name_in_cart, f"Sản phẩm giỏ không đúng: {name_in_cart}"

        order_page.go_to_cart()
        order_page.click_checkout()
        order_page.click_no_invoice()
        order_page.fill_customer_info(fullname, email, phone, address)
        order_page.select_province(province)
        order_page.select_district(district)
        order_page.select_ward(ward)
        order_page.click_continue()
        order_page.click_complete_order_btn()

        from selenium.common.exceptions import TimeoutException

        try:
            WebDriverWait(driver, 10).until(
                lambda d: len(order_page.get_message_text()) > 0
                          or order_page.get_success_message() != ""
            )
        except TimeoutException:
            pass

        errors = order_page.get_message_text()  # trả về list lỗi
        if errors:
            actual_result = errors[0]  # lấy lỗi đầu tiên
        else:
            # Nếu không có lỗi, kiểm tra thông báo đặt hàng thành công
            actual_result = order_page.get_success_message()
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
