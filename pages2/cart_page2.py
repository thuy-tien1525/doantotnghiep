from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.btn_add = (By.XPATH, "//button[contains(@class,'add_to_cart')]")
        self.popup_checkout_btn = ( By.XPATH,"//a[normalize-space()='Thanh toán']")

        self.text_cart = (By.CSS_SELECTOR, ".text2line.link")
        self.product_name = (By.CLASS_NAME, "title-product")

        self.btn_minus = (By.CSS_SELECTOR, ".reduced items-count btn-minus btn")
        self.btn_plus = (By.CSS_SELECTOR, ".increase items-count btn-plus btn")
        self.btn_remove = (By.CSS_SELECTOR, "a[title='Xóa']")
        self.input_number = (By.CSS_SELECTOR, "#qtyMobile1164003405")
        self.total_price = (By.CSS_SELECTOR, ".text-xs-right  totals_price_mobile")
        self.text_active = (By.XPATH, "//li[@class='active']")


    def get_product_name(self):
        try:
            name = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.product_name)
            ).text
            print(f"Tên sản phẩm trước khi thêm: {name}")
            return name
        except TimeoutException:
            raise Exception("Không tìm thấy tên sản phẩm!")

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
    def get_text_in_cart(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.text_cart)
            )
            name_in_cart = element.text.strip()
            print(f"Sản phẩm trong giỏ: {name_in_cart}")
            return name_in_cart
        except TimeoutException:
            raise Exception("Không tìm thấy tên sản phẩm trong giỏ hàng!")


