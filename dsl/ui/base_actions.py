from playwright.sync_api import Page
from helpers.common import Settings as settings, load_yaml, yaml_files, get_absolute_path
from helpers.ui_helpers import initiate_browser


class BaseActions:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_page(self, url):
        self.page.goto(url)


if __name__ == "__main__":
    for yaml_file in yaml_files:
        file = get_absolute_path(yaml_file)
        load_yaml(file)
    page = initiate_browser()
    BaseActions(page).navigate_to_page(settings.pages['total_jobs']['home'])
