import re
from dsl.ui.base_actions import BaseActions
from helpers.common import Settings as settings
from playwright._impl._api_types import TimeoutError


class Job(BaseActions):
    def __init__(self):
        super().__init__(settings.page)
        self.locators = settings.locators['indeed']['job_page']

    @property
    def title(self):
        return self.get_text(self.locators['job_title'])

    @property
    def location(self):
        return self.get_text(self.locators['location'])

    @property
    def salary(self):
        try:
            return self.get_text(self.locators['salary'])
        except TimeoutError:
            return 'Not found'

    @property
    def role_type(self):
        try:
            return self.get_text(self.locators['role_type'])
        except TimeoutError:
            return 'Not found'

    @property
    def description(self):
        return self.get_text(self.locators['job_description'])

    @property
    def employer(self):
        return self.get_text(self.locators['employer'])

    @property
    def apply_on_company_site(self):
        try:
            self.page.get_by_role("button", name=re.compile('apply on company site', re.IGNORECASE))
            return True
        except TimeoutError:
            return False
