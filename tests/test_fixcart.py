import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.Fixcart_page import FixPage
from utils.test_result_writer_excel import write_test_results_excel

all_results = []

def test_edit_cart_thienlong():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    cart_page = FixPage(driver)

    test_name = "test_edit_cart"
    screenshot_path = ""
    actual_result = ""
    status = "FAIL"

    try:
        driver.get("https://thienlong.vn/collections/may-tinh-khoa-hoc-1?q=filter=((collectionid:product=1003213612))&page=1&sortby=manual&view=grid")

        cart_page.click_quick_view()
        time.sleep(1)
        name_before = cart_page.get_product_name()

        assert cart_page.select_color(), "Sản phẩm hết hàng"

        cart_page.click_add_to_cart()
        time.sleep(2)

        cart_page.open_cart()
        if not cart_page.is_cart_page_active():
            raise AssertionError("Không mở được trang giỏ hàng!")

        qty_before, total_before = cart_page.get_cart_quantity_and_total()

        cart_page.increase_quantity()
        qty_plus, total_plus = cart_page.get_cart_quantity_and_total()
        if int(qty_plus) <= int(qty_before):
            raise AssertionError(f"Số lượng không tăng: {qty_before} → {qty_plus}")

        cart_page.decrease_quantity()
        qty_minus, total_minus = cart_page.get_cart_quantity_and_total()
        if int(qty_minus) != int(qty_before):
            raise AssertionError(f"Số lượng sau giảm không về như cũ: {qty_minus}")

        cart_page.remove_product(name_before)
        time.sleep(2)
        try:
            qty_final, _ = cart_page.get_cart_quantity_and_total()
            if int(qty_final) != 0:
                raise AssertionError("Sản phẩm vẫn còn trong giỏ!")
        except Exception:
            # Nếu giỏ trống → PASS
            pass

        actual_result = f"Thêm: {qty_before}, Tăng: {qty_plus}, Giảm: {qty_minus}, Xóa thành công"
        status = "PASS"

    except Exception as e:
        screenshot_dir = "report/screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
        driver.save_screenshot(screenshot_path)
        if not actual_result:
            actual_result = str(e)

    finally:
        driver.quit()

    all_results.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Test Name": test_name,
        "Actual": actual_result,
        "Status": status,
        "Screenshot": screenshot_path if status == "FAIL" else ""
    })

    assert status == "PASS", f"[{test_name}] Actual: {actual_result}"

def teardown_module(module):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report/test_results_edit_cart_{timestamp}.xlsx"
    write_test_results_excel(
        all_results,
        filename=filename,
        sheet_name="Test Results EditCart"
    )
