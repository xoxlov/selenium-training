import time
import pytest
from selenium import webdriver

@pytest.fixture
def browser(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def validate_stickers_separately(browser):
    tabs = browser.find_elements_by_css_selector("a[data-toggle='tab']")
    for tab in range(len(tabs)):
        browser.find_elements_by_css_selector("a[data-toggle='tab']")[tab].click()
        items = browser.find_elements_by_css_selector("div.tab-content div[style=''] div.image-wrapper")
        # Problem: в текущей конфигурации пропускается элемент с одной уточкой (закладка самая первая), хотя
        # в обычном поиске всё работает как надо. Единственным найденным способом для различия табов оказалось
        # использование стилей, а точнее, отсутствие такового у активной закладки.
        for item in range(len(items)):
            sticker = items[item].find_elements_by_css_selector("div")
            assert(len(sticker) == 1)
            items = browser.find_elements_by_css_selector("div.tab-content div[style=''] div.image-wrapper")

def validate_stickers_all_at_once(browser):
    items = browser.find_elements_by_css_selector("div.image-wrapper")
    for item in range(len(items)):
        items = browser.find_elements_by_css_selector("div.image-wrapper")
        sticker = items[item].find_elements_by_css_selector("div")
        assert(len(sticker) == 1)

def test_function(browser):
    browser.get("http://localhost/litecart/")
    # initial page has 3 tabs - go through them and validate separately
    validate_stickers_separately(browser)
    # but all items are present on the page - validate them without clicking tabs
    validate_stickers_all_at_once(browser)
