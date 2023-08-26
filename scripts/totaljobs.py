from data.constants import NEWLY_POSTED_STRING
from dsl.ui.base_actions import BaseActions
from dsl.ui.pages.totaljobs.home import HomePage
from dsl.ui.pages.totaljobs.job import Job
from dsl.ui.pages.totaljobs.search_results import SearchResults
from helpers.common import yaml_files, get_absolute_path, load_yaml
from helpers.ui_helpers import initiate_browser
from helpers.common import Settings as settings
import re
import math


class Bot:
    DESIRED_JOB_TYPE = 'Permanent'
    MINIMUM_SALARY = 10000
    REQUIRED_SKILLS_AND_EXP = ['python', 'github', 'docker', 'bash', 'powershell', 'terraform', 'jenkins']
    SKILL_MATCH_THRESHOLD = 80
    JOBS_LESS_THAN = 17

    def setup_browser(self):
        for yaml_file in yaml_files:
            file = get_absolute_path(yaml_file)
            load_yaml(file)
        settings.page = initiate_browser()
        BaseActions(settings.page)
        settings.total_home = HomePage()
        settings.search = SearchResults()

    def __evaluate_date_posted(self):
        settings.job = Job()
        if settings.job.date_posted == NEWLY_POSTED_STRING:
            settings.apply_for_job = True
            print('Job was recently posted, proceed ...')
        else:
            # Using regular expression to extract the integer
            match = re.search(r'\d+', settings.job.date_posted)
            date_posted = int(match.group())
            if date_posted < self.MINIMUM_SALARY:
                settings.apply_for_job = True
                print('Job was recently posted, proceed ...')
            else:
                print(f'job is too old as it was posted {date_posted} days ago')

    def __evaluate_job_type(self):
        if settings.job.role_type == self.DESIRED_JOB_TYPE:
            settings.apply_for_job = True
            print(f'Job type is {settings.job.role_type} as requested, proceed ...')
        else:
            print(f'Oops wrong job type:{settings.job.role_type}')

    def __evaluate_job_salary(self):
        matches = re.findall(r'£\d+', settings.job.salary)
        if len(matches) >= 2:
            actual_salary = eval(matches[1].replace('£', ''))
            if actual_salary > self.MINIMUM_SALARY:
                settings.apply_for_job = True
                print(f'Job salary: {settings.job.salary} meets requirements, proceed ...')
            else:
                settings.apply_for_job = False
                print(f'Oops job salary: {settings.job.salary} does not meet requirements'
                      f'(not greater than £{self.MINIMUM_SALARY})')
        else:
            settings.apply_for_job = False
            print(f'Oops job salary: {settings.job.salary} cannot be evaluated')

    def __evaluate_job_description(self):
        count_present = sum(1 for element in self.REQUIRED_SKILLS_AND_EXP if element.lower() in settings.job.description.lower())
        percentage_present = math.ceil((count_present / len(self.REQUIRED_SKILLS_AND_EXP)) * 100)
        if percentage_present >= self.SKILL_MATCH_THRESHOLD:
            settings.apply_for_job = True
            print(f"{percentage_present}% of your skills and experience match this job posting, proceed...")
        else:
            settings.apply_for_job = False
            print(f"Opps! You meet only {percentage_present}% of the skills required for this position")

    def evaluate_job(self):
        settings.apply_for_job = False
        self.__evaluate_date_posted()
        self.__evaluate_job_type()
        self.__evaluate_job_salary()
        self.__evaluate_job_description()

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
            self.evaluate_job()
            if not settings.apply_for_job:
                print('Job posting is either too old or does not meet expectations of applicant')
                break
            settings.search.click_on_element(button='Apply')
            settings.search.wait_for_locator(settings.locators['total_jobs']['application_page']['email_address'])

            settings.search.send_text(locator=settings.locators['total_jobs']['application_page']['email_address'],
                                      text='emailaddressofbotapper@gmail.com')
            settings.search.click_on_element(button='continue with email')
            settings.search.send_text(locator=settings.locators['total_jobs']['application_page']['password'],
                                      text="HardtoguessP333")
            settings.search.click_on_element(button='continue application')
            #
            # settings.search.click_on_element(
            #     locator=settings.locators['total_jobs']['application_page']['apply_with_cv'])
            # settings.search.file_chooser("")


if __name__ == "__main__":
    bot = Bot()
    bot.setup_browser()
    bot.search_for_job(job_title='devops engineer', location='London')
