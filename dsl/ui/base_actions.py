import re
from playwright.sync_api import Page


class BaseActions:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_page(self, url):
        self.page.goto(url)

    def click_on_element(self, **kwargs):
        if kwargs.get('button'):
            self.page.get_by_role("button", name=re.compile(kwargs['button'], re.IGNORECASE)).click()
        elif kwargs.get('locator'):
            self.page.locator(kwargs['locator']).click()
        else:
            raise ValueError('Invalid element')

    def send_text(self, locator, text):
        self.page.fill(locator, text)

    def get_text(self, locator):
        return self.page.text_content(locator)

    def previous_page(self):
        self.page.go_back()
