from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RegisterPage:
    def __init__(self, driver):
        self.driver = driver
        self.last_name_input = (By.ID, "lastName")
        self.first_name_input = (By.ID, "firstName")
        self.email_input = (By.ID, "email")
        self.phone_input = (By.ID, "Phone")
        self.password_input = (By.ID, "password")
        self.register_btn = (By.XPATH, "//button[contains(text(),'Đăng ký')]")
        self.success = (By.CSS_SELECTOR, ".success-message")
        self.error_toast = (By.CSS_SELECTOR, ".toast-message")
        self.error_html5 = (By.XPATH, "//li[contains(text(),'Yêu cầu không hợp lệ, hoặc quá hạn, phiền bạn thử ')]")


    def register(self, first_name="", last_name="", email="", phone="", password=""):
        self.driver.find_element(*self.first_name_input).clear()
        self.driver.find_element(*self.first_name_input).send_keys(first_name or "")

        self.driver.find_element(*self.last_name_input).clear()
        self.driver.find_element(*self.last_name_input).send_keys(last_name or "")

        self.driver.find_element(*self.email_input).clear()
        self.driver.find_element(*self.email_input).send_keys(email or "")

        self.driver.find_element(*self.phone_input).clear()
        self.driver.find_element(*self.phone_input).send_keys(phone or "")

        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password or "")

        self.driver.find_element(*self.register_btn).click()

    def get_message(self, first_name, last_name, email, phone, password, timeout=3):
        # Required fields
        if not first_name:
            return self.driver.find_element(*self.first_name_input).get_attribute("validationMessage")
        if not last_name:
            return self.driver.find_element(*self.last_name_input).get_attribute("validationMessage")
        if not email:
            return self.driver.find_element(*self.email_input).get_attribute("validationMessage")
        if not phone:
            return self.driver.find_element(*self.phone_input).get_attribute("validationMessage")
        if not password:
            return self.driver.find_element(*self.password_input).get_attribute("validationMessage")

        email_validation = self.driver.find_element(*self.email_input).get_attribute("validationMessage")
        if email_validation:
            return email_validation

        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text.strip()
            alert.accept()
            return text
        except TimeoutException:
            pass

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toast-message"))
            )
            return element.text.strip()
        except TimeoutException:
            pass
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.error_html5)
            )
            return element.text.strip()
        except TimeoutException:
            pass

        return "Không tìm thấy thông báo"


