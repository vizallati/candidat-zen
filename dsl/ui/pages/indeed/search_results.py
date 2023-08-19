from dsl.ui.base_actions import BaseActions
from dsl.ui.pages.indeed.home import HomePage
from helpers.common import Settings as settings, yaml_files, get_absolute_path, load_yaml
from helpers.ui_helpers import initiate_browser


class SearchResults(BaseActions):
    def __init__(self):
        super().__init__(settings.page)
        self.locators = settings.locators['indeed']['results_page']

    def wait_for_results(self):
        self.page.wait_for_selector(self.locators['job_cards'])


def test_search_results_pom():
    for yaml_file in yaml_files:
        file = get_absolute_path(yaml_file)
        load_yaml(file)
    settings.page = initiate_browser()
    BaseActions(settings.page)
    indeed_home = HomePage()
    search_results = SearchResults()
    indeed_home.search_for_job(position='devops engineer', location='Birmingham')
    search_results.wait_for_results()
