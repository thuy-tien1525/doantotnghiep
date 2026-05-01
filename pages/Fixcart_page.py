from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

class FixPage:
    def __init__(self, driver):
        self.driver = driver
        self.quick_view = (By.XPATH, "//body[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/form[1]/div[2]/div[4]/div[1]/a[1]/span[1]")
        self.phanloai_mau = (By.XPATH, "//input[@id='swatch-0-trang']")
        self.btn_add = (By.CSS_SELECTOR, ".add_to_cart")
        self.product_name = (By.XPATH, "//a[@class='text2line']")
        self.cart_icon = (By.XPATH, "//a[@title='Giỏ hàng']")

        self.text_active = (By.XPATH, "//li[contains(@class,'active') or contains(text(),'Giỏ hàng')]")

    def click_quick_view(self):
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.quick_view))
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
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.cart_icon)).click()
        print(" Đã mở trang giỏ hàng.")
        time.sleep(2)

    def increase_quantity(self):
        try:
            qty_input = self.driver.find_element(By.CSS_SELECTOR, "input.number-sidebar")
            old_val = qty_input.get_attribute("value")

            btn_plus_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'btn-plus')]/i[contains(@class,'fa-plus')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_plus_icon)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", btn_plus_icon)

            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(By.CSS_SELECTOR, "input.number-sidebar").get_attribute("value") != old_val
            )
            new_val = self.driver.find_element(By.CSS_SELECTOR, "input.number-sidebar").get_attribute("value")
            print(f"Số lượng tăng từ {old_val} → {new_val}")
        except Exception as e:
            print(f"Không tăng được số lượng: {e}")

    def decrease_quantity(self):
        try:
            qty_input = self.driver.find_element(By.CSS_SELECTOR, "input.number-sidebar")
            old_val = qty_input.get_attribute("value")

            btn_minus_icon = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class,'btn-minus')]/i[contains(@class,'fa-minus')]"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_minus_icon)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", btn_minus_icon)

            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(By.CSS_SELECTOR, "input.number-sidebar").get_attribute("value") != old_val
            )
            new_val = self.driver.find_element(By.CSS_SELECTOR, "input.number-sidebar").get_attribute("value")
            print(f"Số lượng giảm từ {old_val} → {new_val}")
        except Exception as e:
            print(f"Không giảm được số lượng: {e}")

    def remove_product(self, product_name):
        try:
            btn_remove = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     f"//a[contains(text(),'{product_name}')]/ancestor::tr//button[contains(@class,'remove')]")
                )
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_remove)
            time.sleep(5)
            btn_remove.click()
            time.sleep(10)

            print(f"Sản phẩm '{product_name}' đã được xóa thành công!")
        except TimeoutException:
            print(f"Không tìm thấy sản phẩm '{product_name}' trong giỏ → đã xóa thành công.")
        except Exception as e:
            print(f"Lỗi khi xóa sản phẩm: {e}")
            raise

    def get_cart_quantity_and_total(self):
        try:
            qty_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.number-sidebar"))
            )
            total_price_el = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.totals_price_mobile"))
            )

            qty = int(qty_input.get_attribute("value").strip())
            total = total_price_el.text.strip()
            print(f"Số lượng: {qty}, Tổng tiền: {total}")
            return qty, total
        except Exception as e:
            print(f"Không lấy được số lượng hoặc tổng tiền: {e}")
            raise

    def is_cart_page_active(self):
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.text_active)
            )
            text = el.text.strip()
            print(f" Breadcrumb hiện tại: {text}")
            return "Giỏ hàng" in text
        except TimeoutException:
            print(" Không tìm thấy breadcrumb 'Giỏ hàng'.")
            return False
