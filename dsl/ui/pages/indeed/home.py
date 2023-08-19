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


def test_home_pom():
    for yaml_file in yaml_files:
        file = get_absolute_path(yaml_file)
        load_yaml(file)
    settings.page = initiate_browser()
    BaseActions(settings.page)
    total_home = HomePage()
    total_home.search_for_job(position='cloud engineer', location='Bedworth')

