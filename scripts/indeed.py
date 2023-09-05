from dsl.ui.base_actions import BaseActions
from dsl.ui.pages.indeed.home import HomePage
from dsl.ui.pages.indeed.job import Job
from dsl.ui.pages.indeed.search_results import SearchResults
from helpers.common import yaml_files, get_absolute_path, load_yaml
from helpers.ui_helpers import initiate_browser
from helpers.common import Settings as settings
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

    def setup_browser(self):
        for yaml_file in yaml_files:
            file = get_absolute_path(yaml_file)
            load_yaml(file)
        settings.page = initiate_browser()
        BaseActions(settings.page)
        settings.indeed_home = HomePage()
        settings.search = SearchResults()

    def __evaluate_possibility_to_apply(self):
        settings.job = Job()
        if settings.job.apply_on_company_site:
            settings.apply_for_job = False
            print("Job cannot be made on indeed's website ...")
        else:
            settings.apply_for_job = True
            print("Job application can be be made on indeed's website, proceed ...")

    def __evaluate_job_type(self):
        settings.job = Job()
        if self.DESIRED_JOB_TYPE in settings.job.role_type:
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
        count_present = sum(
            1 for element in self.REQUIRED_SKILLS_AND_EXP if element.lower() in settings.job.description.lower())
        percentage_present = math.ceil((count_present / len(self.REQUIRED_SKILLS_AND_EXP)) * 100)
        if percentage_present >= self.SKILL_MATCH_THRESHOLD:
            settings.apply_for_job = True
            print(f"{percentage_present}% of your skills and experience match this job posting, proceed...")
        else:
            settings.apply_for_job = False
            print(f"Opps! You meet only {percentage_present}% of the skills required for this position")

    def evaluate_job(self):
        settings.apply_for_job = False
        self.__evaluate_possibility_to_apply()
        self.__evaluate_job_type()
        self.__evaluate_job_salary()
        self.__evaluate_job_description()

    def search_for_job(self, job_title, location):
        settings.indeed_home.navigate_to_page(settings.pages['indeed']['home'])
        settings.indeed_home.send_text(settings.locators['indeed']['home_page']['job_title'], job_title)
        settings.indeed_home.send_text(settings.locators['indeed']['home_page']['location'], location)
        settings.indeed_home.click_on_element(button='find jobs')
        settings.search.wait_for_results()
        settings.search.click_on_element(locator=settings.locators['indeed']['home_page']['close_pop_up'])
        settings.indeed_home.click_on_element(locator=settings.locators['indeed']['home_page']['accept_cookies'])
        jobs_to_apply = 0
        while jobs_to_apply < 25:
            all_jobs = settings.page.query_selector_all(settings.locators['indeed']['results_page']['job_cards'])
            number_of_jobs = len(all_jobs)
            results_url = settings.page.url

            for index in range(number_of_jobs):
                all_jobs[index].click()
                self.evaluate_job()

                if not settings.apply_for_job:
                    print('Job posting is either too old or does not meet expectations of applicant')
                    settings.search.navigate_to_page(results_url)
                    all_jobs = settings.page.query_selector_all(
                        settings.locators['indeed']['results_page']['job_cards'])
                    continue  # Continue to the next job posting

                jobs_to_apply += 1
                print(f'Jobs applied for {jobs_to_apply}')
                settings.search.click_on_element(button='Apply')

                settings.search.navigate_to_page(results_url)
                all_jobs = settings.page.query_selector_all(
                    settings.locators['indeed']['results_page']['job_cards'])
                continue


if __name__ == "__main__":
    bot = Bot(job_type='Permanent', minimum_salary=10000,
              required_skills=['python', 'github', 'docker', 'bash', 'powershell', 'terraform', 'jenkins'],
              match_threshold=80, date_posted=17,email='',first_name='',surname='',password='')
    bot.setup_browser()
    bot.search_for_job(job_title='devops engineer', location='London')
