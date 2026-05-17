from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class OrderPage:
    def __init__(self, driver):
        self.driver = driver
        self.quick_view = (By.XPATH,"//body[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/form[1]/div[2]/div[4]/div[1]/a[1]/span[1]")
        self.phanloai_mau = (By.XPATH, "//input[@id='swatch-0-trang']")
        self.btn_add = (By.CSS_SELECTOR, ".add_to_cart")
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
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.cart_icon)
        ).click()

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
        # Chờ select huyện hiển thị
        district_select = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(By.ID, "customer_shipping_district")
        )
        # Chờ option mong muốn load xong
        WebDriverWait(self.driver, 15).until(
            lambda d: any(opt.text.strip() == district_name for opt in
                          Select(d.find_element(By.ID, "customer_shipping_district")).options)
        )
        select = Select(district_select)
        select.select_by_visible_text(district_name)

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
        button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".step-footer-continue-btn")
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            button
        )

        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".step-footer-continue-btn")
                )
            )
            button.click()

        except:
            self.driver.execute_script(
                "arguments[0].click();",
                button
            )

    def get_message_text(self, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".field-message.field-message-error")
                )
            )
            return [el.text.strip() for el in elements if el.text.strip()]
        except TimeoutException:
            return []

    def get_success_message(self, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.success_text)
            )
            return element.text.strip()
        except TimeoutException:
            return None
