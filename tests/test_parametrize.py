"""
Переопределите параметр с помощью indirect параметризации на уровне теста
"""
import pytest
from selene import have
from selene.support.shared import browser
from selenium import webdriver


@pytest.fixture(params=[(1080, 1920), (800, 480)], ids=['desktop', 'mobile'])
def browser_fixture(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    browser.config.driver_options = options
    browser.config.window_height = request.param[0]
    browser.config.window_width = request.param[1]
    browser.config.base_url = 'https://github.com'
    yield
    browser.quit()


@pytest.mark.parametrize('browser_fixture', [pytest.param((1080, 1920), id='desktop')], indirect=True)
def test_github_desktop(browser_fixture):
    browser.open('/')
    browser.element('a[href="/login"]').click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))


@pytest.mark.parametrize('browser_fixture', [pytest.param((800, 480), id='mobile')], indirect=True)
def test_github_mobile(browser_fixture):
    browser.open('/')
    browser.element('[aria-label="Toggle navigation"] > .Button-content').click()
    browser.element('a[href="/login"]').click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))
