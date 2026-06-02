from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.ID, "customer_email")
        self.password_input = (By.ID, "customer_password")
        self.login_btn = (By.XPATH, "//button[contains(text(),'Đăng nhập')]")
        self.error = (By.CSS_SELECTOR, ".toast-message")
        self.error_html5 = (By.XPATH, "//div[@class='form-signup margin-bottom-15']")
        self.greeting_text = (By.XPATH, "//a[contains(text(),'Hi,')]")
        self.open_login_btn = (By.CSS_SELECTOR, "a[class='font-weight-bold']")
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

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                self.open_login_btn
            )
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    def login(self, email, password):
        email = email.strip() if email else ""
        password = password.strip() if password else ""

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_input)
        )

        email_element = self.driver.find_element(*self.email_input)
        password_element = self.driver.find_element(*self.password_input)

        email_element.clear()
        email_element.send_keys(email)

        password_element.clear()
        password_element.send_keys(password)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.login_btn)
        ).click()

    def get_error_message(self, email, password, timeout=10):


        if not email or "@" not in email or ".." in email or email.endswith("@") or "@@" in email:
            return self.driver.find_element(*self.email_input).get_attribute("validationMessage")
        if not password:
            return self.driver.find_element(*self.password_input).get_attribute("validationMessage")

        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text.strip()
            alert.accept()
            return text
        except TimeoutException:
            pass

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.error)
            )
            return element.text.strip()
        except TimeoutException:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located(self.error_html5)
                )
                return element.text.strip()
            except TimeoutException:
                pass

        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.greeting_text)
            )
            return element.text.strip()
        except TimeoutException:
            return "Không tìm thấy thông báo"
