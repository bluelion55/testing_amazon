import allure

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from exceptions import BrowserNotInstantiated
from .config import Config


class WebScraper:
    def __init__(self):
        self.browser = None

    def start_browser(
        self,
        headless: bool = Config.HEADLESS,
        chrome_driver_path: str = Config.CHROME_PATH,
        use_further_options: bool = True,
        browser=None,
    ):
        if not self.browser:
            if not browser:
                browser = self._instantiate_chrome_browser(
                    headless,
                    chrome_driver_path,
                    use_further_options,
                )

            self.browser = browser

    def _instantiate_chrome_browser(
        self,
        headless: bool,
        chrome_driver_path: str,
        use_further_options: bool = True,
    ) -> webdriver.Chrome:
        options = ChromeOptions()

        if use_further_options:
            options.add_argument("ignore-certificate-errors")
            options.add_argument("window-size=1920,1080")
            options.add_argument("no-sandbox")
            options.add_argument("start-fullscreen")
            options.add_argument("log-level=0")
            options.add_argument("disable-logging")
            options.add_argument("silent")

        if headless:
            options.add_argument("headless=true")

        return webdriver.Chrome(chrome_options=options, executable_path=chrome_driver_path)

    def get_page(self, url: str) -> None:
        if self.browser:
            self.browser.get(url)
            return
        raise BrowserNotInstantiated()

    def get_html(self) -> Tag:
        if self.browser:
            return BeautifulSoup(self.browser.page_source)
        raise BrowserNotInstantiated()

    def close_browser(self):
        if self.browser:
            self.browser.close()
            print("Closed browser.")
        else:
            print("Browser already closed.")

    def create_new_tab(self, link: str):
        if self.browser is not None:
            self.browser.execute_script(f'window.open("{link}");')
            current_tab = self.browser.current_window_handle
            new_tab = [tab for tab in self.browser.window_handles if tab != current_tab][0]
            self.browser.switch_to.window(new_tab)
            return
        raise BrowserNotInstantiated()
    
    def close_tab(self, handle_idx: int):
        if self.browser is not None:
            tab_to_close = self.browser.window_handles[handle_idx]
            self.browser.switch_to.window(tab_to_close)
            self.browser.close()
            return
        raise BrowserNotInstantiated()
    
    def try_find_element_by_xpath(self, xpath, source=None):
        if self.browser is not None:
            try:
                if source is None:
                    return self.browser.find_element(by=By.XPATH, value=xpath)
                else:
                    return source.find_element(by=By.XPATH, value=xpath)
            except NoSuchElementException:
                return None

    def try_find_elements_by_xpath(self, xpath):
        if self.browser is not None:
            try:
                return self.browser.find_elements(by=By.XPATH, value=xpath)
            except NoSuchElementException:
                return None

    def wait_for_presence_of_element(self, element_xpath: str, seconds: float = 30.) -> None:
        try:
            WebDriverWait(self.browser, seconds).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
        except Exception as err:
            raise Exception(err)

    def click_element(self, locator: str, seconds: float = 30.) -> None:
        self.wait_for_presence_of_element(locator, seconds)
        element = self.try_find_element_by_xpath(locator)
        element.click()

    def take_screenshot(self, name) -> None:
        allure.attach(self.browser.get_screenshot_as_png(), name, attachment_type=allure.attachment_type.PNG)
