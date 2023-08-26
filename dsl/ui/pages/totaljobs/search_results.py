from dsl.ui.base_actions import BaseActions
from helpers.common import Settings as settings


class SearchResults(BaseActions):
    def __init__(self):
        super().__init__(settings.page)
        self.locators = settings.locators['total_jobs']['results_page']

    def wait_for_results(self):
        self.page.wait_for_selector(self.locators['job_cards'])


