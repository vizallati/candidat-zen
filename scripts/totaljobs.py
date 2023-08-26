from dsl.ui.base_actions import BaseActions
from dsl.ui.pages.totaljobs.home import HomePage
from dsl.ui.pages.totaljobs.job import Job
from dsl.ui.pages.totaljobs.search_results import SearchResults
from helpers.common import yaml_files, get_absolute_path, load_yaml
from helpers.ui_helpers import initiate_browser
from helpers.common import Settings as settings
import re


class Bot:

    def setup_browser(self):
        for yaml_file in yaml_files:
            file = get_absolute_path(yaml_file)
            load_yaml(file)
        settings.page = initiate_browser()
        BaseActions(settings.page)
        settings.total_home = HomePage()
        settings.search = SearchResults()

    def __evaluate_date_posted(self):
        newly_posted_string = 'Today'  # move to constants
        settings.job = Job()
        if settings.job.date_posted == newly_posted_string:
            settings.apply_for_job = True
            print('Job was recently posted, proceed ...')
        else:
            # Using regular expression to extract the integer
            match = re.search(r'\d+', settings.job.date_posted)
            date_posted = int(match.group())
            if date_posted < 17:
                settings.apply_for_job = True
                print('Job was recently posted, proceed ...')
            else:
                print(f'job is too old as it was posted {date_posted} days ago')

    def __evaluate_job_type(self):
        desired_job_type = 'Permanent'  # should be accepted as env variable
        if settings.job.role_type == desired_job_type:
            settings.apply_for_job = True
            print(f'Job type is {settings.job.role_type} as requested, proceed ...')
        else:
            print(f'Oops wrong job type:{settings.job.role_type}')

    def evaluate_job(self):
        settings.apply_for_job = False
        self.__evaluate_date_posted()
        self.__evaluate_job_type()

    def search_for_job(self, job_title, location):
        settings.total_home.navigate_to_page(settings.pages['total_jobs']['home'])
        settings.total_home.click_on_element(locator=settings.locators['total_jobs']['home_page']['accept_cookies'])
        settings.total_home.send_text(settings.locators['total_jobs']['home_page']['job_title'], job_title)
        settings.total_home.send_text(settings.locators['total_jobs']['home_page']['location'], location)
        settings.total_home.click_on_element(button='search')
        settings.search.wait_for_results()
        all_jobs = settings.page.query_selector_all(settings.locators['total_jobs']['results_page']['job_cards'])
        for job_posting in all_jobs:
            job_posting.click()
            settings.page.wait_for_load_state()
            self.evaluate_job()
            if not settings.apply_for_job:
                print('Job posting is either too old or does not meet expectations of applicant')
                break
            settings.search.click_on_element(button='Apply')
            settings.search.wait_for_locator(settings.locators['total_jobs']['application_page']['email_address'])

            # settings.search.send_text(locator=settings.locators['total_jobs']['application_page']['email_address'],
            #                           text='')
            # settings.search.click_on_element(button='continue with email')
            # settings.search.send_text(locator=settings.locators['total_jobs']['application_page']['password'],
            #                           text="")
            # settings.search.click_on_element(button='continue application')
            #
            # settings.search.click_on_element(
            #     locator=settings.locators['total_jobs']['application_page']['apply_with_cv'])
            # settings.search.file_chooser("")


if __name__ == "__main__":
    bot = Bot()
    bot.setup_browser()
    bot.search_for_job(job_title='devops engineer', location='London')
    bot.evaluate_job()
