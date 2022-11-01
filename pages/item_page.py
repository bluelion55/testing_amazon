import re

import allure
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By


class ItemPage:

    def __init__(self, scraper):
        self.scraper = scraper

        self.__about_item_section = "//h1[.=' About this item ']"
        self.__item_name = "//span[@id='productTitle']"
        self.__side_info_price_tag = "(//span[@class='a-price-whole'])[1]"
        self.__about_this_item = "//div[@id='feature-bullets']"
        self.__item_details = "//li/span[@class='a-list-item']"

    @allure.step("Check the 'About this item' section")
    def check_about_this_item_section(self) -> None:
        try:
            self.scraper.wait_for_presence_of_element(self.__about_item_section)
        except TimeoutException:
            raise TimeoutException("Could not find the 'About this item' section")
        item_details = self.scraper.try_find_element_by_xpath(self.__about_item_section)
        assert item_details, "The 'About this item' section is not present on the page"

    @allure.step("Check the item name")
    def check_item_name(self, name) -> None:
        self.scraper.wait_for_presence_of_element(self.__item_name)
        item_name_element = self.scraper.try_find_element_by_xpath(self.__item_name)
        assert item_name_element, "The item name is not present on the page"

        item_name = item_name_element.text
        assert item_name == name, f'Expected {name}, got {item_name}'

    @allure.step("Check the item price")
    def check_item_price(self, price) -> None:
        self.scraper.wait_for_presence_of_element(self.__side_info_price_tag)
        price_tag_element = self.scraper.try_find_element_by_xpath(self.__side_info_price_tag)
        assert price_tag_element, "Could not find price tag."

        product_item_price = re.sub(r"[^0-9.,]+", r"", str(price_tag_element.text))
        assert product_item_price == price, f'Expected {price}, got {product_item_price}'

    @allure.step("Check the item details")
    def check_item_details(self) -> list:
        try:
            self.scraper.wait_for_presence_of_element(self.__about_this_item)
        except TimeoutException:
            raise TimeoutException("Could not find the 'About this item' section")
        item_details = self.scraper.try_find_element_by_xpath(self.__about_this_item)

        details = item_details.find_elements(by=By.XPATH, value=self.__item_details)
        details_content = [detail.get_attribute("innerHTML") for detail in details]
        details_content = [detail for detail in details_content if self.__find_iterations_of_tag_pattern(s=detail) == 0]
        item_details = []
        for detail in details_content:
            item_details.append(detail)
        return item_details

    def __find_iterations_of_tag_pattern(self, s: str) -> int:
        return len([m.start() for m in re.finditer(r"<[^>]+>", s)])
