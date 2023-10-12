from data.constants import NEWLY_POSTED_STRING, RECENTLY_POSTED_STRING
from dsl.ui.base_actions import BaseActions
from dsl.ui.pages.totaljobs.home import HomePage
from dsl.ui.pages.totaljobs.job import Job
from dsl.ui.pages.totaljobs.search_results import SearchResults
from helpers.common import yaml_files, get_absolute_path, load_yaml
from helpers.ui_helpers import initiate_browser
from helpers.common import Settings as settings
from loguru import logger
import re
import math


class Bot:
    def __init__(self, job_type, minimum_salary, required_skills, match_threshold, date_posted,
                 email, first_name, surname, password):
        self.DESIRED_JOB_TYPE = job_type
        self.MINIMUM_SALARY = minimum_salary
        self.REQUIRED_SKILLS_AND_EXP = required_skills
        self.SKILL_MATCH_THRESHOLD = match_threshold
        self.JOBS_LESS_THAN = date_posted
        self.first_time_using_email = True
        self.email = email
        self.first_name = first_name
        self.sur_name = surname
        self.password = password
        self.apply_for_job = 0

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
        if settings.job.date_posted == NEWLY_POSTED_STRING or RECENTLY_POSTED_STRING:
            self.apply_for_job += 1
            logger.info('Job was recently posted, proceed ...')
        else:
            # Using regular expression to extract the integer
            match = re.search(r'\d+', settings.job.date_posted)
            date_posted = int(match.group())
            if date_posted < self.JOBS_LESS_THAN:
                self.apply_for_job += 1
                logger.info('Job was recently posted, proceed ...')
            else:
                logger.info(f'job is too old as it was posted {date_posted} days ago')

    def __evaluate_job_type(self):
        if settings.job.role_type == self.DESIRED_JOB_TYPE:
            self.apply_for_job += 1
            logger.info(f'Job type is {settings.job.role_type} as requested, proceed ...')
        else:
            logger.info(f'Oops wrong job type:{settings.job.role_type}')

    def __evaluate_job_salary(self):
        matches = re.findall(r'£\d+', settings.job.salary)
        if len(matches) >= 2:
            actual_salary = eval(matches[1].replace('£', ''))
            if actual_salary > self.MINIMUM_SALARY:
                self.apply_for_job += 1
                logger.info(f'Job salary: {settings.job.salary} meets requirements, proceed ...')
            else:
                logger.info(f'Oops job salary: {settings.job.salary} does not meet requirements'
                            f'(not greater than £{self.MINIMUM_SALARY})')
        else:
            logger.info(f'Oops job salary: {settings.job.salary} cannot be evaluated')

    def __evaluate_job_description(self):
        count_present = sum(
            1 for element in self.REQUIRED_SKILLS_AND_EXP if element.lower() in settings.job.description.lower())
        percentage_present = math.ceil((count_present / len(self.REQUIRED_SKILLS_AND_EXP)) * 100)
        if percentage_present >= self.SKILL_MATCH_THRESHOLD:
            self.apply_for_job += 1
            logger.info(f"{percentage_present}% of your skills and experience match this job posting, proceed...")
        else:
            logger.info(f"Opps! You meet only {percentage_present}% of the skills required for this position")

    def evaluate_job(self):
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
        jobs_to_apply = 0
        while jobs_to_apply < 25:
            all_jobs = settings.page.query_selector_all(settings.locators['total_jobs']['results_page']['job_cards'])
            number_of_jobs = len(all_jobs)
            results_url = settings.page.url

            for index in range(number_of_jobs):
                all_jobs[index].click()
                self.evaluate_job()

                if self.apply_for_job < 4:
                    logger.info('Job posting is either too old or does not meet expectations of applicant')
                    settings.search.navigate_to_page(results_url)
                    all_jobs = settings.page.query_selector_all(
                        settings.locators['total_jobs']['results_page']['job_cards'])
                    self.apply_for_job = 0
                    continue  # Continue to the next job posting

                jobs_to_apply += 1
                logger.info(f'Jobs applied for {jobs_to_apply}')
                settings.search.click_on_element(button='Apply')
                settings.search.wait_for_locator(settings.locators['total_jobs']['application_page']['email_address'])

                settings.search.send_text(locator=settings.locators['total_jobs']['application_page']['email_address'],
                                          text=self.email)

                if self.first_time_using_email:
                    settings.search.click_on_element(button='continue with email')
                    settings.search.send_text(locator=settings.locators['total_jobs']['application_page']['password'],
                                              text=self.password)
                    settings.search.click_on_element(button='continue application')
                else:
                    settings.search.click_on_element(button='continue with email')
                    settings.search.send_text(locator=settings.locators['total_jobs']['application_page']['password'],
                                              text=self.password)
                    settings.search.click_on_element(button='continue without signing in')

                settings.search.click_on_element(
                    locator=settings.locators['total_jobs']['application_page']['apply_with_cv'])
                settings.search.file_chooser(r'')
                settings.search.send_text(locator=settings.locators['total_jobs']['application_page']['first_name'],
                                          text=self.first_name)
                settings.search.send_text(locator=settings.locators['total_jobs']['application_page']['sur_name'],
                                          text=self.sur_name)
                settings.search.select_option(locator=settings.locators['total_jobs']['application_page']['education'],
                                              option='University degree')  # Needs to be passed as param from ui
                settings.search.send_text(
                    locator=settings.locators['total_jobs']['application_page']['most_recent_job'],
                    text='Intern')
                settings.search.select_option(
                    locator=settings.locators['total_jobs']['application_page']['most_recent_salary'],
                    option='26,000-27,999')  # Need to look for a way to get this value by using salary expectations
                settings.search.click_on_element(button='send application')
                settings.search.navigate_to_page(results_url)
                all_jobs = settings.page.query_selector_all(
                    settings.locators['total_jobs']['results_page']['job_cards'])
                self.apply_for_job = 0
                continue


if __name__ == "__main__":
    bot = Bot(job_type='Permanent', minimum_salary=1000000,
              required_skills=['python', 'github', 'docker', 'bash', 'powershell', 'terraform', 'jenkins'],
              match_threshold=80, date_posted=17, email='', first_name='', surname='', password='')
    bot.setup_browser()
    bot.search_for_job(job_title='devops engineer', location='London')
