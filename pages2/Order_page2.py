from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
import time


class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.btn_add = (By.XPATH, "//button[contains(@class,'add_to_cart')]")
        self.popup_checkout_btn = (By.XPATH, "//a[normalize-space()='Thanh toán']")
        self.btn_checkout = (By.CSS_SELECTOR,"button[title='Tiến hành thanh toán']")
        self.input_fullname = (By.ID, "billing_address_full_name")
        self.input_email = (By.ID, "checkout_user_email")
        self.input_phone = (By.ID, "billing_address_phone")
        self.input_address = (By.ID, "billing_address_address1")

        self.tinh_select = (By.ID, "customer_shipping_province")
        self.huyen_select = (By.ID, "customer_shipping_district")
        self.xa_select = (By.ID, "customer_shipping_ward")

        self.continue_btn = (By.CSS_SELECTOR,"button.step-footer-continue-btn.btn")
        self.success_text = (By.XPATH,"//h2[contains(text(),'Đặt hàng thành công')]")
        self.complete_order_btn = (By.XPATH,"//span[contains(text(),'Hoàn tất đơn hàng')]")

    def click_add_to_cart(self):

        wait = WebDriverWait(self.driver, 15)

        # tìm element trước
        btn = wait.until(
            EC.presence_of_element_located(self.btn_add)
        )

        # scroll xuống
        self.driver.execute_script("""
               arguments[0].scrollIntoView({
                   behavior: 'smooth',
                   block: 'center'
               });
           """, btn)

        time.sleep(2)

        # đợi clickable sau khi scroll
        wait.until(
            EC.element_to_be_clickable(self.btn_add)
        )

        try:
            btn.click()
        except Exception as e:
            print("Normal click failed:", e)

            self.driver.execute_script(
                "arguments[0].click();",
                btn
            )

        print("Click add to cart OK")

    def click_checkout_popup(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[normalize-space()='Thanh toán']")
            )
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )
        time.sleep(1)

        try:
            button.click()
        except:
            self.driver.execute_script(
                "arguments[0].click();",
                button
            )
    def click_checkout(self):

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.btn_checkout)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        time.sleep(0.5)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )
    def fill_customer_info(self, fullname, email, phone, address):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.input_fullname)
        ).send_keys(fullname)

        self.driver.find_element(*self.input_email).send_keys(email)
        self.driver.find_element(*self.input_phone).send_keys(phone)
        self.driver.find_element(*self.input_address).send_keys(address)

    def select_province(self, province_name):
        select = Select(self.driver.find_element(*self.tinh_select))
        select.select_by_visible_text(province_name)

        WebDriverWait(self.driver, 10).until(
            lambda d: len(
                Select(
                    d.find_element(*self.huyen_select)
                ).options
            ) > 1
        )

    def select_district(self, district_name):
        district_select = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(
                By.ID,
                "customer_shipping_district"
            )
        )

        WebDriverWait(self.driver, 15).until(
            lambda d: any(
                opt.text.strip() == district_name
                for opt in Select(
                    d.find_element(
                        By.ID,
                        "customer_shipping_district"
                    )
                ).options
            )
        )

        Select(district_select).select_by_visible_text(district_name)

    def select_ward(self, ward_name):
        WebDriverWait(self.driver, 10).until(
            lambda d: any(
                opt.text.strip() == ward_name
                for opt in Select(
                    d.find_element(
                        By.ID,
                        "customer_shipping_ward"
                    )
                ).options
            )
        )

        select = Select(
            self.driver.find_element(
                By.ID,
                "customer_shipping_ward"
            )
        )

        select.select_by_visible_text(ward_name)

    def click_continue(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.continue_btn)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        time.sleep(0.5)

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    def click_complete_order_btn(self):
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(.,'Hoàn tất đơn hàng')]"
                )
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        time.sleep(2)

        try:
            button.click()

        except:
            self.driver.execute_script(
                "arguments[0].click();",
                button
            )

    def get_message_text(self):
        try:
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".field-message")
                )
            )

            return [el.text.strip() for el in elements if el.text.strip()]

        except:
            return []

    def get_success_message(self, timeout=10):

        try:
            element = WebDriverWait(
                self.driver,
                timeout,
                ignored_exceptions=[StaleElementReferenceException]
            ).until(
                EC.visibility_of_element_located(
                    self.success_text
                )
            )

            return element.text.strip()

        except (TimeoutException, StaleElementReferenceException):
            return ""