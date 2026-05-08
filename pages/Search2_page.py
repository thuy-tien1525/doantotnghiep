from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoAlertPresentException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
import time
import re


class Search2Page:

    def __init__(self, driver):

        self.driver = driver

        # menu Văn phòng phẩm
        self.office_menu = (
            By.XPATH,
            "//a[@title='Văn phòng phẩm']//i[@class='fas fa-chevron-down float-right']"
        )

        # filter loại sản phẩm
        self.pen_menu = (
            By.CSS_SELECTOR,
            "//a[@title='Bút lông bảng - lông dầu"
        )

        # filter thương hiệu
        self.brand_filter = (
            By.XPATH,
            "//label[normalize-space()='Colokit']"
        )

        # filter giá
        self.price_filter = (
            By.XPATH,
            "//label[@for='filter-100-000d-300-000d']"
        )

        # tên sản phẩm
        self.product_name = (
            By.XPATH,
            "//body//div//div[@data-sort='manual']//div//div//div//div[2]//div[1]//form[1]"
        )

        # giá sản phẩm
        self.product_price = (
            By.XPATH,
            "//span[@class='price']"
        )

        self.error = (
            By.CSS_SELECTOR,
            ".title-head, .alert, .note, .message, .result"
        )

    def find(self, locator):

        return self.driver.find_element(*locator)

    def finds(self, locator):

        return self.driver.find_elements(*locator)

    def click(self, locator):

        wait = WebDriverWait(self.driver, 20)

        element = wait.until(
            EC.element_to_be_clickable(locator)
        )

        # scroll tới giữa màn hình
        self.driver.execute_script("""
            arguments[0].scrollIntoView({
                block: 'center'
            });
        """, element)

        time.sleep(2)

        try:

            element.click()

        except (
                ElementClickInterceptedException,
                ElementNotInteractableException
        ):

            # fallback JS click
            self.driver.execute_script(
                "arguments[0].click();",
                element
            )

        # chờ ajax load
        time.sleep(4)

    def open_office_menu(self):

        self.click(self.office_menu)

    def choose_pen_filter(self):

        self.click(self.pen_filter)

        time.sleep(3)

    def choose_brand_filter(self):

        self.click(self.brand_filter)

        time.sleep(3)

    def choose_price_filter(self):

        self.click(self.price_filter)

        time.sleep(3)

    def get_product_names(self):

        wait = WebDriverWait(self.driver, 10)

        wait.until(
            EC.presence_of_all_elements_located(
                self.product_name
            )
        )

        products = self.finds(self.product_name)

        names = []

        for product in products:

            text = product.text.strip()

            if text:
                names.append(text)

        return names

    def get_product_prices(self):

        wait = WebDriverWait(self.driver, 10)

        wait.until(
            EC.presence_of_all_elements_located(
                self.product_price
            )
        )

        prices = self.finds(self.product_price)

        result = []

        for price in prices:

            text = price.text.strip()

            text = re.sub(r"[^\d]", "", text)

            if text:
                result.append(int(text))

        return result

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

        if not messages:

            messages.append(
                "Không có thông báo hiển thị."
            )

        return " | ".join(messages)