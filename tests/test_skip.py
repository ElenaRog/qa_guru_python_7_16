"""
Параметризуйте фикстуру несколькими вариантами размеров окна
Пропустите мобильный тест, если соотношение сторон десктопное (и наоборот)
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
    yield request.param
    browser.quit()


def test_github_desktop(browser_fixture):
    if browser_fixture[0] > browser_fixture[1]:
        pytest.skip('Неверное расширение экрана')
    browser.open('/')
    browser.element('a[href="/login"]').click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))


def test_github_mobile(browser_fixture):
    if browser_fixture[0] <= browser_fixture[1]:
        pytest.skip('Неверное расширение экрана')
    browser.open('/')
    browser.element('[aria-label="Toggle navigation"] > .Button-content').click()
    browser.element('a[href="/login"]').click()
    browser.element('.auth-form-header').should(have.exact_text('Sign in to GitHub'))
