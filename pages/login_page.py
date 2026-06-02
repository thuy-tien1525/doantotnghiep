from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

        self.email_input = (By.ID, "customer_email")
        self.password_input = (By.ID, "customer_password")
        self.login_btn = (By.XPATH, "//button[contains(text(),'Đăng nhập')]")

        self.error = (By.CSS_SELECTOR, ".toast-message")
        self.error_html5 = (By.XPATH, "//div[@class='form-signup margin-bottom-15']")

        self.greeting_text = (By.XPATH, "//a[contains(text(),'Hi,')]")

        self.open_login_btn = (By.CSS_SELECTOR, "a.font-weight-bold")

    def open(self, url):
        self.driver.get(url)

    def open_login_form(self):

        element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                self.open_login_btn
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                self.email_input
            )
        )

    def login(self, email, password):

        email = str(email).strip() if email else ""
        password = str(password).strip() if password else ""

        email_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                self.email_input
            )
        )

        password_element = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(
                self.password_input
            )
        )

        email_element.clear()
        email_element.send_keys(email)

        password_element.clear()
        password_element.send_keys(password)

        login_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(
                self.login_btn
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            login_button
        )

    def get_error_message(self, email, password, timeout=20):

        email = str(email).strip() if email else ""
        password = str(password).strip() if password else ""

        # HTML5 validation
        try:
            email_validation = self.driver.find_element(
                *self.email_input
            ).get_attribute("validationMessage")

            if email_validation:
                return email_validation.strip()
        except:
            pass

        try:
            password_validation = self.driver.find_element(
                *self.password_input
            ).get_attribute("validationMessage")

            if password_validation:
                return password_validation.strip()
        except:
            pass

        # Toast lỗi đăng nhập
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    self.error
                )
            )
            return element.text.strip()

        except TimeoutException:
            pass

        # Login thành công
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    self.greeting_text
                )
            )
            return element.text.strip()

        except TimeoutException:
            pass

        return "Không tìm thấy thông báo"