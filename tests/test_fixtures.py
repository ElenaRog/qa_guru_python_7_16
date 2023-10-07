"""
Сделайте разные фикстуры для каждого теста, которые выставят размеры окна браузера
"""
import pytest
from selene import have
from selene.support.shared import browser
from selenium import webdriver

@pytest.fixture
def browser_desktop():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    browser.config.driver_options = options
    browser.config.window_height = 1080
    browser.config.window_width = 1920
    browser.config.base_url = 'https://github.com'
    yield
    browser.quit()


def test_github_desktop(browser_desktop):
    browser.open('/')
    browser.element('a[href="/login"]').click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))




@pytest.fixture
def browser_mobile():
    browser.config.window_height = 800
    browser.config.window_width = 480
    browser.config.base_url = 'https://github.com/'
    yield
    browser.quit()


def test_github_mobile(browser_mobile):
    browser.open('/')
    browser.element('[aria-label="Toggle navigation"] > .Button-content').click()
    browser.element('a[href="/login"]').click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))

