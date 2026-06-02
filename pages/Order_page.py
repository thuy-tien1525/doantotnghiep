from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException,ElementClickInterceptedException,StaleElementReferenceException)
import time


class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.quick_view = (By.XPATH, "(//a[@title='Xem nhanh'])[1]")
        self.phanloai_mau = (By.XPATH, "//input[@id='swatch-0-trang']")
        self.btn_add = (By.XPATH, "//div[contains(@class,'quickview-product')]//button[@type='submit']")
        self.cart_icon = (By.XPATH, "//a[@title='Giỏ hàng']")
        self.btn_checkout = (By.XPATH, "//button[@title='Tiến hành đặt hàng']")
        self.no_invoice_btn = (By.XPATH, "//button[contains(text(),'Không xuất hóa đơn và đến trang Thanh toán')]")

        self.input_fullname = (By.ID, "billing_address_full_name")
        self.input_email = (By.ID, "checkout_user_email")
        self.input_phone = (By.ID, "billing_address_phone")
        self.input_address = (By.ID, "billing_address_address1")

        self.tinh_select = (By.ID, "customer_shipping_province")
        self.huyen_select = (By.ID, "customer_shipping_district")
        self.xa_select = (By.ID, "customer_shipping_ward")

        self.continue_btn = (By.CSS_SELECTOR, "button.step-footer-continue-btn.btn")
        self.success_text = (By.XPATH, "//h2[contains(text(),'Đặt hàng thành công')]")
        self.error_message = (By.CSS_SELECTOR, ".toast-message")
        self.complete_order_btn = (By.XPATH, "//button[@class='step-footer-continue-btn btn']")

    def go_to_cart(self):
        for _ in range(3):
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.cart_icon)
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    element
                )

                element.click()
                return

            except ElementClickInterceptedException:

                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located(
                        (By.CSS_SELECTOR, ".swal-overlay")
                    )
                )

        raise Exception("Cannot click cart icon")

    def click_checkout(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.btn_checkout)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(2)
        self.driver.execute_script("arguments[0].click();", element)

    def click_no_invoice(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.no_invoice_btn)
        ).click()
        time.sleep(5)
    def fill_customer_info(self, fullname, email, phone, address):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.input_fullname)
        ).send_keys(fullname)
        self.driver.find_element(*self.input_email).send_keys(email)
        self.driver.find_element(*self.input_phone).send_keys(phone)
        self.driver.find_element(*self.input_address).send_keys(address)
        time.sleep(5)

    def select_province(self, province_name):
        select = Select(self.driver.find_element(*self.tinh_select))
        select.select_by_visible_text(province_name)
        time.sleep(2)

        WebDriverWait(self.driver, 10).until(
            lambda d: len(Select(d.find_element(*self.huyen_select)).options) > 1
        )

    def select_district(self, district_name):

        WebDriverWait(self.driver, 15).until(
            lambda d: any(
                opt.text.strip() == district_name
                for opt in Select(
                    d.find_element(*self.huyen_select)
                ).options
            )
        )

        Select(
            self.driver.find_element(*self.huyen_select)
        ).select_by_visible_text(district_name)

    def select_ward(self, ward_name):
        WebDriverWait(self.driver, 10).until(
            lambda d: any(opt.text.strip() == ward_name for opt in
                          Select(d.find_element(By.ID, "customer_shipping_ward")).options)
        )
        select = Select(self.driver.find_element(By.ID, "customer_shipping_ward"))
        select.select_by_visible_text(ward_name)

    def click_continue(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.step-footer-continue-btn.btn"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(2)

    def click_complete_order_btn(self):

        for _ in range(3):

            try:
                button = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(
                        self.complete_order_btn
                    )
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    button
                )

                self.driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                return

            except StaleElementReferenceException:
                time.sleep(1)

        raise Exception("Cannot click complete order button")
    def get_message_text(self, timeout=10):

        def clean_message(msg):
            if not msg:
                return ""

            msg = msg.strip()

            if msg.lower() in ["message:", "message"]:
                return ""

            return msg

        messages = []

        # HTML5 validation
        fields = [
            self.input_fullname,
            self.input_email,
            self.input_phone,
            self.input_address,
        ]

        for field in fields:
            validation = ""

            try:
                el = self.driver.find_element(*field)
                validation = el.get_attribute("validationMessage") or ""
                validation = validation.strip()
            except StaleElementReferenceException:
                continue
            except Exception:
                continue

            if validation and validation not in messages:
                messages.append(validation)
        # Field error message
        try:
            elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".field-message.field-message-error"
            )

            for el in elements:
                try:
                    text = clean_message(el.text)

                    if text and text not in messages:
                        messages.append(text)

                except StaleElementReferenceException:
                    continue

        except Exception:
            pass

        # Toast message
        try:
            toast_elements = self.driver.find_elements(
                By.CSS_SELECTOR,
                ".toast-message"
            )

            for el in toast_elements:
                try:
                    text = clean_message(el.text)

                    if text and text not in messages:
                        messages.append(text)

                except StaleElementReferenceException:
                    continue

        except Exception:
            pass

        return messages

    def get_success_message(self, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.success_text)
            )

            return element.text.strip()

        except (
                TimeoutException,
                StaleElementReferenceException
        ):
            return ""

        except Exception:
            return ""
