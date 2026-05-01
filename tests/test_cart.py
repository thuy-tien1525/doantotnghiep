import time
import os
import pytest
from datetime import datetime
from pages.cart_page import CartPage
from utils.test_result_writer_excel import write_test_results_excel

# List lưu kết quả test
all_results = []

@pytest.mark.parametrize("index,url,expected_product", [
    (1, "https://thienlong.vn/collections/may-tinh-khoa-hoc-1?q=filter=((collectionid:product=1003213612))&page=1&sortby=manual&view=grid",
     "Máy tính khoa học Thiên Long Flexio Fx509VN - Có hơn 240 tính năng")
])
def test_add_to_cart(browser, index, url, expected_product):
    driver = browser
    cart_page = CartPage(driver)

    driver.get(url)
    driver.maximize_window()

    test_name = f"test_add_to_cart_{index}"
    screenshot_path = ""
    actual_result = ""
    status = "FAIL"

    try:
        # Click nhanh xem sản phẩm
        cart_page.click_quick_view()
        time.sleep(2)

        assert cart_page.select_color(), "Sản phẩm hết hàng"
        # Lấy tên sản phẩm trước khi thêm
        product_name = cart_page.get_product_name()

        # Thêm vào giỏ
        cart_page.click_add_to_cart()
        time.sleep(2)

        # Mở giỏ hàng
        cart_page.open_cart()
        time.sleep(2)

        name_in_cart = cart_page.get_text_in_cart()
        actual_result = name_in_cart


        if product_name.strip().lower() in name_in_cart.strip().lower():
            status = "PASS"
        else:
            raise AssertionError(f"Expected {product_name}, Actual {name_in_cart}")

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
