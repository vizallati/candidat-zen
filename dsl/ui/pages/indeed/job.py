from dsl.ui.base_actions import BaseActions
from helpers.common import Settings as settings


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
        return self.get_text(self.locators['salary'])

    @property
    def role_type(self):
        return self.get_text(self.locators['role_type'])

    @property
    def description(self):
        return self.get_text(self.locators['job_description'])

    @property
    def employer(self):
        return self.get_text(self.locators['employer'])
