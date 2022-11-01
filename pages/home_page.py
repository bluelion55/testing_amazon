import allure
from retry import retry
from selenium.common import ElementClickInterceptedException
from selenium.webdriver import ActionChains


class Homepage:

    def __init__(self, scraper):
        self.scraper = scraper
        self.__amazon_logo = "//a[@id='nav-logo-sprites']"
        self.__hamburger_menu_button = "//a[@id='nav-hamburger-menu']"
        self.__hamburger_menu = "//ul[@class='hmenu hmenu-visible']"
        self.__see_all_dept = "//a[@class='hmenu-item hmenu-compressed-btn']"
        self.__computers = "//div[.='Computers']/.."
        self.__computers_section_title = "//div[@class='hmenu-item hmenu-title ' and text()='computers']"
        self.__monitors = "//a[.='Monitors']"

    @allure.step("Wait for Amazon logo to be present")
    def wait_for_logo(self) -> None:
        self.scraper.wait_for_presence_of_element(self.__amazon_logo)

    @allure.step("Click hamburger menu button and verify the menu is open")
    def open_hamburger_menu(self) -> None:
        self.scraper.wait_for_presence_of_element(self.__hamburger_menu_button)
        self.scraper.click_element(self.__hamburger_menu_button)
        self.scraper.wait_for_presence_of_element(self.__hamburger_menu)

    @allure.step("Click 'See all' button")
    def expand_all_items(self) -> None:
        self.scraper.wait_for_presence_of_element(self.__see_all_dept)
        self.scraper.click_element(self.__see_all_dept)

    @allure.step("Select Computers department")
    @retry(ElementClickInterceptedException, delay=1, tries=5)
    def select_computers_section(self) -> None:
        self.scraper.wait_for_presence_of_element(self.__computers)
        computers_element = self.scraper.try_find_element_by_xpath(self.__computers)
        actions = ActionChains(self.scraper.browser)
        actions.move_to_element(computers_element).perform()
        computers_element.click()
        self.scraper.wait_for_presence_of_element(self.__computers_section_title)

    @allure.step("Select Monitors section from Computers department")
    def select_monitors_section(self) -> None:
        self.scraper.wait_for_presence_of_element(self.__monitors)
        self.scraper.click_element(self.__monitors)
