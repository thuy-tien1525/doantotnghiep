from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.quick_view = (By.XPATH, "//body[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/form[1]/div[2]/div[4]/div[1]/a[1]/span[1]")
        self.phanloai_mau = (By.XPATH, "//input[@id='swatch-0-trang']")
        self.btn_add = (By.CSS_SELECTOR, ".add_to_cart")
        self.cart_icon = (By.XPATH, "//a[@title='Giỏ hàng']")
        self.text_cart = (By.XPATH, "//a[@class='text2line']")
        self.product_name = (By.XPATH, "//a[@class='text2line']")

        self.btn_minus = (By.CSS_SELECTOR, "reduced items-count btn-minus btn")
        self.btn_plus = (By.CSS_SELECTOR, "increase items-count btn-plus btn")
        self.btn_remove = (By.CSS_SELECTOR, "remove-itemx remove-item-cart")
        self.input_number = (By.CSS_SELECTOR, "form-control input-text number-sidebar qtyMobile1151929586")
        self.total_price = (By.CSS_SELECTOR, "text-xs-right  totals_price_mobile")
        self.text_active = (By.XPATH, "//li[@class='active']")

    def click_quick_view(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.quick_view)
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        element.click()

    def get_product_name(self):
        try:
            name = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.product_name)
            ).text
            print(f"Tên sản phẩm trước khi thêm: {name}")
            return name
        except TimeoutException:
            raise Exception("Không tìm thấy tên sản phẩm!")

    def select_color(self):
        try:
            el = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.phanloai_mau)
            )

            # lấy label cha
            parent = el.find_element(By.XPATH, "./..")
            class_attr = parent.get_attribute("class").lower()

            if "soldout" in class_attr or "disabled" in class_attr:
                print(" Màu trắng hết hàng")
                return False

            self.driver.execute_script("arguments[0].click();", el)
            print(" Đã chọn màu trắng")
            return True

        except Exception as e:
            print(" Không chọn được màu:", e)
            return False
    def click_add_to_cart(self):
        wait = WebDriverWait(self.driver, 10)

        btn = wait.until(EC.element_to_be_clickable(self.btn_add))

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", btn
        )

        try:
            btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", btn)

        print("Click add to cart OK")

    def open_cart(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.cart_icon)
        ).click()
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


