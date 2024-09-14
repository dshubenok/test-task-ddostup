import logging
import time

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GoogleAuth:
    def __init__(self, desired_caps: dict[str, str] | None = None) -> None:
        """
        Инициализация класса GoogleAuth.
        :param desired_caps: Словарь с желаемыми настройками для Appium. Если не указан, используются значения по умолчанию.
        """
        self.desired_caps: dict[str, str] = desired_caps or {
            'platformName': 'Android',
            'deviceName': 'Android Emulator',
            'appPackage': 'com.google.android.gm',
            'appActivity': 'com.google.android.gm.ConversationListActivityGmail',
            'automationName': 'UiAutomator2'
        }
        self.driver: webdriver.Remote = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.wait: WebDriverWait = WebDriverWait(self.driver, 15)

    def login(self, email: str, password: str) -> None:
        """
        Выполняет процесс входа в Gmail.
        :param email: Адрес электронной почты для входа.
        :param password: Пароль для входа.
        """
        try:
            self.driver.activate_app('com.google.android.gm')
            time.sleep(5)

            if self.is_welcome_screen():
                self.skip_welcome_screen()

            if self.is_already_logged_in():
                self.handle_logged_in_state()
            else:
                self.perform_login(email, password)

            if self.is_authenticated():
                logger.info("Вход выполнен успешно")
            else:
                logger.error("Ошибка входа")
        except Exception as e:
            self.handle_error(e)

    def is_welcome_screen(self) -> bool:
        """Проверяет, находится ли пользователь на экране приветствия."""
        return self.element_exists('com.google.android.gm:id/welcome_tour_got_it')

    def skip_welcome_screen(self) -> None:
        """Пропускает экран приветствия."""
        self.click_element('com.google.android.gm:id/welcome_tour_got_it')

    def is_already_logged_in(self) -> bool:
        """Проверяет, вошел ли пользователь уже в систему."""
        return self.element_exists('//*[@text="TAKE ME TO GMAIL"]')

    def handle_logged_in_state(self) -> None:
        """Обрабатывает состояние, когда пользователь уже вошел в систему."""
        self.click_element('//*[@text="TAKE ME TO GMAIL"]')
        self.click_element('com.android.permissioncontroller:id/permission_deny_button')
        self.click_element('//*[@text="Got it"]')

    def perform_login(self, email: str, password: str) -> None:
        """
        Выполняет процесс входа в систему.
        :param email: Адрес электронной почты для входа.
        :param password: Пароль для входа.
        """
        self.click_element('com.google.android.gm:id/setup_addresses_add_another')
        self.click_element('//android.widget.TextView[@text="Google"]')
        self.input_text('//android.widget.EditText[@resource-id="identifierId"]', email)
        self.click_element('//android.widget.Button[@text="Next"]')
        self.input_text('//android.widget.EditText[@password="true"]', password)
        time.sleep(2)
        self.click_element('//android.widget.Button[@text="Next"]')
        self.click_element('//android.widget.Button[@text="I agree"]')
        self.click_element('//android.widget.Button[@text="Accept"]')
        self.click_element('//android.widget.Button[@text="TAKE ME TO GMAIL"]')
        time.sleep(3)

    def is_authenticated(self) -> bool:
        """Проверяет, успешно ли выполнена аутентификация."""
        auth_elements: list[str] = [
            'com.google.android.gm:id/conversation_list_view',
            'com.google.android.gm:id/compose_button',
            '//*[@text="Inbox" or @text="Primary"]'
        ]
        return any(self.element_exists(elem) for elem in auth_elements)

    def handle_error(self, error: Exception) -> None:
        """
        Обрабатывает ошибки, возникающие во время процесса входа.
        :param error: Объект исключения.
        """
        logger.error(f"Произошла ошибка при входе: {str(error)}")
        logger.info(f"Текущая активность: {self.driver.current_activity}")
        logger.info(f"Текущий пакет: {self.driver.current_package}")

    def element_exists(self, locator: str) -> bool:
        """
        Проверяет существование элемента на странице.
        :param locator: Локатор элемента.
        :return: True, если элемент существует, иначе False.
        """
        try:
            self.wait.until(
                EC.presence_of_element_located((MobileBy.XPATH if '//' in locator else MobileBy.ID, locator)))
            return True
        except:
            return False

    def click_element(self, locator: str) -> None:
        """
        Кликает по элементу.
        :param locator: Локатор элемента.
        """
        self.wait.until(
            EC.element_to_be_clickable((MobileBy.XPATH if '//' in locator else MobileBy.ID, locator))).click()

    def input_text(self, locator: str, text: str) -> None:
        """
        Вводит текст в элемент.
        :param locator: Локатор элемента.
        :param text: Текст для ввода.
        """
        element: WebElement = self.wait.until(
            EC.presence_of_element_located((MobileBy.XPATH if '//' in locator else MobileBy.ID, locator)))
        element.clear()
        element.send_keys(text)

    def close(self) -> None:
        """Закрывает драйвер."""
        if hasattr(self, 'driver'):
            self.driver.quit()
