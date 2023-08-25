import pytest

from dsl.ui.base_actions import BaseActions
from dsl.ui.pages.totaljobs.home import HomePage as total_home
from dsl.ui.pages.totaljobs.search_results import SearchResults as total_search
from dsl.ui.pages.indeed.home import HomePage as indeed_home
from dsl.ui.pages.indeed.search_results import SearchResults as indeed_search
from helpers.common import yaml_files, get_absolute_path, load_yaml
from helpers.ui_helpers import initiate_browser
from helpers.common import Settings as settings


@pytest.fixture(scope='session')
def browser():
    for yaml_file in yaml_files:
        file = get_absolute_path(yaml_file)
        load_yaml(file)
    settings.page = initiate_browser()
    BaseActions(settings.page)


def test_total_home_pom(browser):
    home = total_home()
    home.search_for_job(position='cloud engineer', location='Bedworth')


def test_total_search_results_pom(browser):
    home = total_home()
    search = total_search()
    home.search_for_job(position='cloud engineer', location='Bedworth')
    search.wait_for_results()


def test_indeed_home_pom():
    home = indeed_home()
    home.search_for_job(position='cloud engineer', location='Bedworth')


def test_indeed_search_results_pom():
    home = indeed_home()
    search = indeed_search()
    home.search_for_job(position='devops engineer', location='Birmingham')
    search.wait_for_results()
