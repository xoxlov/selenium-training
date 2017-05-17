import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def browser(request):
    wd = webdriver.Chrome()
    #request.addfinalizer(wd.quit)
    return wd


def do_login_admin(browser):
    wait = WebDriverWait(browser, 10) # 10 seconds

    login_field = browser.find_element_by_name("username")
    login_field.clear()
    login_field.send_keys("admin")

    password_field = browser.find_element_by_name("password")
    password_field.clear()
    password_field.send_keys("admin")
    browser.find_element_by_css_selector('button[name="login"]').click()
    wait.until(EC.title_is("My Store"))
    # wait to be sure the page was loaded completely
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li#widget-discussions")))

def run_through_menu(browser):
    # find elements from menu on the left
    menu_items = browser.find_elements_by_css_selector("li[id='app-']")
    for item in range(len(menu_items)):
        # click at the current menu element
        menu_items[item].click()
        submenu_links = browser.find_elements_by_css_selector(".docs li")
        # if there are subitems - look through them
        if (submenu_links != []):
            # go through every submenu item and click it
            for subitem in range(len(submenu_links)):
                submenu_links[subitem].click()
                header = browser.find_elements_by_tag_name("h1")
                # header can be printed, but its value cannot be decoded as string - problem!
                assert(len(header))
                # re-find elements of submenu to keep actual handlers
                submenu_links = browser.find_elements_by_css_selector(".docs li")
        # continue searching menu items to deal with the actual page elements
        menu_items = browser.find_elements_by_css_selector("li[id='app-']")

def test_function(browser):
    browser.get("http://localhost/litecart/admin/")
    # make login as admin
    do_login_admin(browser)

    # click all the menu items on the left
    run_through_menu(browser)
