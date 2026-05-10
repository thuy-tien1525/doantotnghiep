import os
import pytest
from utils.excel_reader import read_excel_data
from pages.Search_page import SearchPage
from utils.test_result_writer_excel import write_test_results_excel
from datetime import datetime


test_data = read_excel_data("Data/Search_data.xlsx", "Search_data")
all_results = []

@pytest.mark.parametrize("index,keyword,expected_result", [
    (i + 1, *row) for i, row in enumerate(test_data)
])
def test_search(browser, index, keyword, expected_result):
    driver = browser
    search_page = SearchPage(driver)


    driver.get("https://thienlong.vn/")

    test_name = f"test_search_{index}"
    screenshot_path = ""
    actual_result = ""
    status = "FAIL"

    try:
        if keyword.strip() == "":

            search_page.search(keyword)

            actual_result = search_page.get_error()

        else:

            search_page.search(keyword)

            actual_result = search_page.get_search_result()
        if expected_result.strip().lower() in actual_result.strip().lower():
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
        "Keyword": keyword,
        "Expected": expected_result,
        "Actual": actual_result,
        "Status": status,
        "Screenshot": screenshot_path if status == "FAIL" else ""
    })

    assert status == "PASS", f"[{test_name}] Expected: {expected_result}, Actual: {actual_result}"

def teardown_module(module):
    filename = "report/test_results_search.xlsx"
    write_test_results_excel(
        all_results,
        filename=filename,
        sheet_name="Test Results Search"
    )

