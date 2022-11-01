import logging
import time

import pytest

from utils.scraper import WebScraper
from pages.home_page import Homepage
from pages.monitors_page import MonitorsResultsPage
from pages.item_page import ItemPage

logger = logging.getLogger(__name__)


class TestAmazonScraping:

    @pytest.fixture
    def test_init(self):
        self.scraper = WebScraper()
        self.home = Homepage(self.scraper)
        self.monitors = MonitorsResultsPage(self.scraper)
        self.item = ItemPage(self.scraper)
        self.scraper.start_browser()
        self.scraper.get_page("https://amazon.com")
        yield
        self.scraper.browser.quit()

    def test_01_verify_amazon_second_high_priced_item(self, test_init):
        """ To verify the second highest priced item in the Monitors section under the Computers section, verify that
        the item name and price displayed in the item's card and on the item's page matches.

        :param test_init: set up the browser instance, initialise page object
        :return: None
        """
        logger.info("Wait for Amazon logo to be present")
        self.home.wait_for_logo()
        self.scraper.take_screenshot('homepage')

        logger.info("Click hamburger menu button and verify the menu is open")
        self.home.open_hamburger_menu()

        logger.info("Click 'See all' button")
        self.home.expand_all_items()
        self.scraper.take_screenshot('menu')

        logger.info("Select Computers department")
        self.home.select_computers_section()

        logger.info("Select Monitors section from Computers department")
        self.home.select_monitors_section()

        logger.info("Select LG brand from available brands")
        self.monitors.select_lg_brand()
        self.scraper.take_screenshot('unsorted_results')

        logger.info("Sort items from High to low price")
        self.monitors.sort_items_high_to_low()
        self.scraper.take_screenshot('sorted_results')

        logger.info("Retrieve the item's title and price")
        item_info = self.monitors.get_item_info()

        logger.info("Open second item in a new window")
        self.monitors.open_second_item_in_new_tab()
        self.scraper.take_screenshot('item_in_new_tab')

        logger.info("Check the 'About this item' section")
        self.item.check_about_this_item_section()

        logger.info("Check item name")
        self.item.check_item_name(item_info[0])

        logger.info("Check item price")
        self.item.check_item_price(item_info[1])

        logger.info("Check item details")
        details = self.item.check_item_details()

        logger.info(details)
        self.scraper.take_screenshot('item_view')

        time.sleep(5)
