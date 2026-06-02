from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RegisterPage:
    def __init__(self, driver):
        self.driver = driver

        self.first_name_input = (By.ID, "firstName")
        self.last_name_input = (By.ID, "lastName")
        self.email_input = (By.ID, "email")
        self.phone_input = (By.ID, "Phone")
        self.password_input = (By.ID, "password")

        self.register_btn = (By.XPATH, "//button[contains(text(),'Đăng ký')]")

        self.error_message = (By.CSS_SELECTOR, ".toast-message, .error, .invalid-feedback")

    def register(self, first_name="", last_name="", email="", phone="", password=""):

        self.driver.find_element(*self.first_name_input).clear()
        self.driver.find_element(*self.first_name_input).send_keys(first_name)

        self.driver.find_element(*self.last_name_input).clear()
        self.driver.find_element(*self.last_name_input).send_keys(last_name)

        self.driver.find_element(*self.email_input).clear()
        self.driver.find_element(*self.email_input).send_keys(email)

        self.driver.find_element(*self.phone_input).clear()
        self.driver.find_element(*self.phone_input).send_keys(phone)

        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.register_btn)
        ).click()

    def get_message(self, timeout=10):

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.error_message)
            )
            text = element.text.strip()

            return text if text else "NO_MESSAGE"

        except Exception:
            return "NO_MESSAGE"