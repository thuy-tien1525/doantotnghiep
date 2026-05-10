from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.common.keys import Keys

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_input = (By.XPATH, "//input[@placeholder='Tìm kiếm sản phẩm...']")
        self.search_btn = (By.XPATH, "//span[contains(@class,'fa-search')]")
        self.error = (By.CSS_SELECTOR, ".title-head, .alert, .note, .message, .result")

    def find(self, locator):
        return self.driver.find_element(*locator)

    def search(self, keyword):
        wait = WebDriverWait(self.driver, 10)
        input_box = wait.until(EC.element_to_be_clickable(self.search_input))
        input_box.clear()
        input_box.send_keys(keyword)
        input_box.send_keys(Keys.ENTER)

    def get_error_message(self):
        try:
            input_el = self.find(self.search_input)
            message = self.driver.execute_script(
                "return arguments[0].validationMessage;", input_el
            )
            return message.strip() if message else ""
        except Exception:
            return ""

    def get_error(self):
        wait = WebDriverWait(self.driver, 5)
        messages = []
        try:
            elems = self.driver.find_elements(*self.error)
            for el in elems:
                text = el.text.strip()
                if text and text not in messages:
                    messages.append(text)
        except Exception:
            pass

        try:
            alert = self.driver.switch_to.alert
            messages.append(alert.text.strip())
            alert.accept()
        except NoAlertPresentException:
            pass

        html5_msg = self.get_error_message()
        if html5_msg and html5_msg not in messages:
            messages.append(html5_msg)
        if not messages:
            messages.append("Không có thông báo hiển thị.")

        return " | ".join(messages)

