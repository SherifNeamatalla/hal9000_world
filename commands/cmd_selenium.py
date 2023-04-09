from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from commands.cmd_interface import ICmd


class CmdSelenium(ICmd):
    def __init__(self):
        self.driver = self._create_headless_browser()

    def execute(self, cmd_args, cmd_type=None):
        if cmd_type is None:
            raise ValueError("cmd_type must be specified")

        cmd_map = {
            "find_element": self.find_element,
            "click_element": self.click_element,
            "fill_form": self.fill_form,
            "extract_text": self.extract_text,
            "select_option": self.select_option,
            "switch_to_frame": self.switch_to_frame,
            "switch_to_default_content": self.switch_to_default_content,
            "find_elements": self.find_elements,
            "get_url_content": self.get_url_content,
            "navigate_to_url": self.navigate_to_url,
            "fill_search_input": self.fill_search_input,
            "quit": self.quit
        }

        cmd = cmd_map.get(cmd_type)
        if cmd is None:
            raise ValueError(f"Unsupported cmd_type: {cmd_type}")

        result = cmd(**cmd_args)

        return result

    def fill_search_input(self, search_input_selector, search_term):
        search_input = self.driver.find_element('css selector', search_input_selector)
        search_input.clear()
        search_input.send_keys(search_term)
        search_input.send_keys(Keys.RETURN)

    def _create_headless_browser(self):
        firefox_options = Options()
        firefox_options.headless = True
        driver = webdriver.Firefox(options=firefox_options)
        return driver

    def navigate_to_url(self, url):
        self.driver.get(url)
        return "Navigated !"

    def get_url_content(self, url):
        self.driver.get(url)
        return self.driver.page_source

    def find_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return "Not found!"

    def click_element(self, element):
        element = self.driver.find_element('xpath', element)
        element.click()
        return "Clicked !"

    def fill_form(self, element, text):
        element = self.driver.find_element('xpath', element)
        element.clear()
        element.send_keys(text)
        return 'Filled !'

    def extract_text(self, element):
        element = self.driver.find_element('xpath', element)
        return element.text

    def select_option(self, element, option_value):
        from selenium.webdriver.support.ui import Select
        element = self.driver.find_element('xpath', element)
        select = Select(element)
        select.select_by_value(option_value)
        return 'Selected !'

    def switch_to_frame(self, element):
        element = self.driver.find_element('xpath', element)
        self.driver.switch_to.frame(element)
        return 'Switched !'

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
        return 'Switched !'

    def quit(self):
        self.driver.quit()
        return 'Quit !'

    def find_elements(self, by, value, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except TimeoutException:
            return []
