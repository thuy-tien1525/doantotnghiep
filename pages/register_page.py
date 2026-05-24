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

    def close_modal_if_present(self):
        try:
            wait = WebDriverWait(self.driver, 5)

            modal = self.driver.find_elements(By.CLASS_NAME, "modal-tc")
            if modal:
                # thử click nút đóng nếu có
                try:
                    close_btn = self.driver.find_element(
                        By.CSS_SELECTOR,
                        ".modal-tc .close, .modal-tc .btn-close, .modal-tc button"
                    )
                    close_btn.click()
                except:
                    # fallback: remove luôn modal
                    self.driver.execute_script("""
                        document.querySelector('.modal-tc.open')?.remove();
                    """)
        except:
            pass

    def handle_overlays(self):
        try:
            # xoá modal / popup / overlay
            self.driver.execute_script("""
                document.querySelectorAll('.modal-tc, .modal, .overlay, .popup')
                    .forEach(el => el.remove());
            """)

            # mở scroll nếu bị khóa (fullscreen modal hay dùng)
            self.driver.execute_script("""
                document.body.style.overflow = 'auto';
            """)

            # scroll xuống để tránh sticky header che nút
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        except:
            pass
    def register(self, first_name="", last_name="", email="", phone="", password=""):

        self.handle_overlays()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.first_name_input)).clear()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.first_name_input)).send_keys(first_name or "")

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

        def clean_message(msg):
            if not msg:
                return ""

            msg = msg.strip()

            # bỏ message rác
            if msg.lower() in ["message:", "message"]:
                return ""

            return msg

        # Required fields
        if not first_name:
            return clean_message(
                self.driver.find_element(*self.first_name_input)
                .get_attribute("validationMessage")
            )

        if not last_name:
            return clean_message(
                self.driver.find_element(*self.last_name_input)
                .get_attribute("validationMessage")
            )

        if not email:
            return clean_message(
                self.driver.find_element(*self.email_input)
                .get_attribute("validationMessage")
            )

        if not phone:
            return clean_message(
                self.driver.find_element(*self.phone_input)
                .get_attribute("validationMessage")
            )

        if not password:
            return clean_message(
                self.driver.find_element(*self.password_input)
                .get_attribute("validationMessage")
            )

        # Email format validation
        email_validation = clean_message(
            self.driver.find_element(*self.email_input)
            .get_attribute("validationMessage")
        )

        if email_validation:
            return email_validation

        # Browser alert
        try:
            WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert

            text = clean_message(alert.text)

            alert.accept()

            if text:
                return text

        except TimeoutException:
            pass

        # Toast message
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".toast-message"))
            )

            text = clean_message(element.text)

            if text:
                return text

        except TimeoutException:
            pass

        # HTML error
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.error_html5)
            )

            text = clean_message(element.text)

            if text:
                return text

        except TimeoutException:
            pass

        return "Không tìm thấy thông báo"


