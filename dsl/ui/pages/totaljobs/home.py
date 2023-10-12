from loguru import logger

from dsl.ui.base_actions import BaseActions
from helpers.common import Settings as settings


class HomePage(BaseActions):
    def __init__(self):
        super().__init__(settings.page)
        self.locators = settings.locators['total_jobs']['home_page']

    def search_for_job(self, position, location):
        self.navigate_to_page(url=settings.pages['total_jobs']['home'])
        try:
            self.click_on_element(locator=self.locators['accept_cookies'])
        except Exception:
            logger.info('No cookies found')
        self.send_text(self.locators['job_title'], position)
        self.send_text(self.locators['location'], location)
        self.click_on_element(button='search')

