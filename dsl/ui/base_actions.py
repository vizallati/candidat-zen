import re
from playwright.sync_api import Page
from helpers.common import Settings as settings


class BaseActions:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_page(self, url):
        self.page.goto(url)

    def click_on_element(self, **kwargs):
        if kwargs.get('button'):
            self.page.get_by_role("button", name=re.compile(kwargs['button'], re.IGNORECASE)).last.click()
        elif kwargs.get('locator'):
            self.page.locator(kwargs['locator']).click()
        elif kwargs.get('text'):
            self.page.get_by_text(kwargs['text']).click()
        else:
            raise ValueError('Invalid element')

    def send_text(self, locator, text):
        self.page.fill(locator, text)

    def get_text(self, locator):
        return self.page.text_content(locator).strip()

    def previous_page(self):
        self.page.go_back()

    def file_chooser(self, path_to_file):
        # Todo refactor to take element to click on as param
        with self.page.expect_file_chooser() as fc_info:
            self.click_on_element(locator=settings.locators['total_jobs']['application_page']['upload_cv'])
        file_chooser = fc_info.value
        file_chooser.set_files(path_to_file)
