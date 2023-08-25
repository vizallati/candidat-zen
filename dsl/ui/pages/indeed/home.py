from dsl.ui.base_actions import BaseActions
from helpers.common import Settings as settings, yaml_files, get_absolute_path, load_yaml
from helpers.ui_helpers import initiate_browser


class HomePage(BaseActions):
    def __init__(self):
        super().__init__(settings.page)
        self.locators = settings.locators['indeed']['home_page']

    def search_for_job(self, position, location):
        self.navigate_to_page(url=settings.pages['indeed']['home'])
        self.send_text(self.locators['job_title'], position)
        self.send_text(self.locators['location'], location)
        self.click_on_element(button='find jobs')

