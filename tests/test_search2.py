import os
from datetime import datetime

from pages.Search2_page import Search2Page


all_results = []


def test_search2(browser):

    driver = browser

    driver.maximize_window()

    driver.get(
        "https://thienlong.vn/collections/all"
    )

    search2_page = Search2Page(driver)

    test_name = "test_search2"

    screenshot_path = ""

    actual_result = ""

    status = "FAIL"

    try:

        # mở menu
        search2_page.open_office_menu()

        # filter loại sản phẩm
        search2_page.choose_pen_filter()

        product_names = (
            search2_page.get_product_names()
        )

        for name in product_names:

            assert (
                "bảng" in name.lower()
                or
                "lông dầu" in name.lower()
            ), f"Sai sản phẩm: {name}"

        # filter thương hiệu
        search2_page.choose_brand_filter()

        product_names = (
            search2_page.get_product_names()
        )

        for name in product_names:

            assert "colokit" in name.lower(), \
                f"Sai thương hiệu: {name}"

        # filter giá
        search2_page.choose_price_filter()

        prices = (
            search2_page.get_product_prices()
        )

        for price in prices:

            assert 100000 <= price <= 300000, \
                f"Giá không đúng: {price}"

        actual_result = "Filter hoạt động đúng"

        status = "PASS"

    except Exception as e:

        screenshot_dir = "report/screenshots"

        os.makedirs(
            screenshot_dir,
            exist_ok=True
        )

        screenshot_path = os.path.join(
            screenshot_dir,
            f"{test_name}.png"
        )

        driver.save_screenshot(
            screenshot_path
        )

        actual_result = str(e)

    all_results.append({

        "Time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "Test Name": test_name,

        "Actual": actual_result,

        "Status": status,

        "Screenshot": screenshot_path
    })

    assert status == "PASS", \
        f"Actual Result: {actual_result}"