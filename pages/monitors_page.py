import re
import time

import allure


class MonitorsResultsPage:

    def __init__(self, scraper):
        self.scraper = scraper

        self.__lg_link = "//a[.='LG']"
        self.__sort_by_dropdown = "//span[@data-action='a-dropdown-button']"
        self.__dropdown_menu = "//div[@class='a-popover-inner']"
        self.__price_high_to_low = "//a[.='Price: High to Low']"
        self.__second_item = "(//a[@class='a-link-normal s-no-outline'])[2]"
        self.__second_item_title = "(//span[@class='a-size-base-plus a-color-base a-text-normal'])[2]"
        self.__second_item_price = "(//span[@class='a-price-whole'])[2]"

    @allure.step("Select LG brand from available brands")
    def select_lg_brand(self) -> None:
        self.scraper.wait_for_presence_of_element(self.__lg_link)
        self.scraper.click_element(self.__lg_link)
        time.sleep(2)

    @allure.step("Sort items from High to low price")
    def sort_items_high_to_low(self) -> None:
        time.sleep(2)
        self.scraper.wait_for_presence_of_element(self.__sort_by_dropdown)
        self.scraper.click_element(self.__sort_by_dropdown)
        time.sleep(2)
        try:
            self.scraper.wait_for_presence_of_element(self.__price_high_to_low, 10)
        except:
            self.scraper.click_element(self.__sort_by_dropdown)
        finally:
            self.scraper.click_element(self.__price_high_to_low)

    @allure.step("Open second item in a new window")
    def open_second_item_in_new_tab(self) -> None:
        ahref = self.scraper.try_find_element_by_xpath(self.__second_item)
        second_item_url = str(ahref.get_attribute("href"))
        self.scraper.create_new_tab(link=second_item_url)

    def get_item_info(self) -> tuple:
        item_name_element = self.scraper.try_find_element_by_xpath(self.__second_item_title)
        item_name = item_name_element.text
        price_tag_element = self.scraper.try_find_element_by_xpath(self.__second_item_price)
        item_price = re.sub(r"[^0-9.,]+", r"", str(price_tag_element.text))
        return item_name, item_price
