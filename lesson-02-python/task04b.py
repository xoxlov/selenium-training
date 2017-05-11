import time
import pytest
from selenium import webdriver

@pytest.fixture
def browser(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def validate_stickers_separately(browser):
    print("\nChecking stickers count separately tab by tab..")
    function_result = True
    tabs = browser.find_elements_by_css_selector("a[data-toggle='tab']")
    for tab in range(len(tabs)):
        browser.find_elements_by_css_selector("a[data-toggle='tab']")[tab].click()
        # products list, corresponds to the selected tab
        products = browser.find_elements_by_css_selector(".tab-pane")[tab]
        # list goods displayed on the tab (in the products list)
        goods = products.find_elements_by_css_selector("div.image-wrapper")
        amount = len(goods)
        result = True
        for item in range(amount):
            sticker = goods[item].find_elements_by_css_selector("div")
            result = (len(sticker) == 1) and result
            goods = browser.find_elements_by_css_selector("div.tab-content div[style=''] div.image-wrapper")
        print("Stickers count on the tab %s is correct (found %s stickers): " % (tab, amount), end="")
        print("Passed" if (result == True) else "Failed")
        function_result = function_result and result
    print("Stickers count validation: ", end="")
    print("Passed" if (function_result == True) else "Failed")
    return function_result

def validate_stickers_all_at_once(browser):
    print("\nChecking stickers count all together..")
    result = True

    products = browser.find_elements_by_css_selector(".product")
    for item in range ((len(products))):
        sticker = products[item].find_elements_by_css_selector(".sticker")
        result = (len(sticker) == 1) and result
    print("Stickers count validation (found %s stickers): " % len(products), end="")
    print("Passed" if result else "Failed")
    return result

def test_function(browser):
    print()
    browser.get("http://localhost/litecart/")
    overall_result = True
    # initial page has 3 tabs - go through them and validate separately
    overall_result = validate_stickers_separately(browser) and overall_result
    # but all items are present on the page - validate them without clicking tabs
    overall_result = validate_stickers_all_at_once(browser) and overall_result

    print("\n\nOverall result: Passed" if overall_result else "Overall result: Failed")
