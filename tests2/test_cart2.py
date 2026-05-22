import time
import os
import pytest
from datetime import datetime
from pages2.cart_page2 import CartPage
from utils.test_result_writer_excel import write_test_results_excel

all_results = []

@pytest.mark.parametrize("index,url,expected_product", [
    (1, "https://savani.vn/products/ao-thun-ngan-tay-co-tron-nam-mtsa502s6",
     "Áo thun nam ngắn tay cổ tròn hình in trước ngực")
])
def test_add_to_cart(browser, index, url, expected_product):
    driver = browser
    cart_page2 = CartPage(driver)

    driver.get(url)
    driver.maximize_window()

    test_name = f"test_add_to_cart_{index}"
    screenshot_path = ""
    actual_result = ""
    status = "FAIL"

    try:
        product_name = cart_page2.get_product_name()

        cart_page2.click_add_to_cart()
        time.sleep(2)

        cart_page2.click_checkout_popup()
        time.sleep(1)

        name_in_cart = cart_page2.get_text_in_cart()

        actual_result = name_in_cart

        if product_name.lower() in name_in_cart.lower():
            status = "PASS"
        else:
            raise AssertionError(
                f"Expected: {expected_product}, Actual: {name_in_cart}"
            )
    except Exception as e:
        # Lưu screenshot khi fail
        screenshot_dir = "report/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)
        if not actual_result:
            actual_result = str(e)


    all_results.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Name": test_name,
        "URL": url,
        "Expected": expected_product,
        "Actual": actual_result,
        "Status": status,
        "Screenshot": screenshot_path if status == "FAIL" else ""
    })

    assert status == "PASS", f"[{test_name}] Expected: {expected_product}, Actual: {actual_result}"


def teardown_module(module):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report/test_results_add_to_cart_{timestamp}.xlsx"
    write_test_results_excel(
        all_results,
        filename=filename,
        sheet_name="Test Results AddToCart"
    )
