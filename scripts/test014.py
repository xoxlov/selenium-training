import pytest
import time

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import common
import common_litecart

@pytest.fixture
def browser_Chrome(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def check_multi_windows(browser):
    # Done: 1) зайти в админку
    # Done: 2) открыть пункт меню Countries (или страницу http://localhost/litecart/admin/?app=countries&doc=countries)
    # Done: 3) открыть на редактирование какую-нибудь страну или начать создание новой
    # Done: 4) возле некоторых полей есть ссылки с иконкой в виде квадратика со стрелкой -- они ведут на внешние страницы и открываются в новом окне, именно это и нужно проверить.
    # Done: требуется именно кликнуть по ссылке, чтобы она открылась в новом окне, потом переключиться в новое окно, закрыть его, вернуться обратно, и повторить эти действия для всех таких ссылок.
    common.start("Checking multiple windows on countries")
    function_result = True
    wait10 = WebDriverWait(browser, 10)

    common_litecart.do_login_admin(browser)
    browser.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    wait10.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name=disable]")))
    common.success("Countries page opened")

    browser.find_element_by_link_text("Add New Country").click()
    common.success("New country add page opened")

    # find all links targeting new window and go through them
    for i in range(len(browser.find_elements_by_css_selector(".fa-external-link"))):
        common.info("")
        # take another link
        current_element = browser.find_elements_by_css_selector(".fa-external-link")[i]
        # get handles of all windows and current window
        start_handles = set(browser.window_handles)
        start_active_handle = browser.current_window_handle
        # click on the link to open new window
        current_element.click()
        WebDriverWait(browser, 30).until(EC.new_window_is_opened(list(start_handles)))
        # get handles of windows and find new one
        next_handles = set(browser.window_handles)
        new_handle = next_handles ^ start_handles
        common.info("New window id = %s" % list(new_handle)[0])
        # switch to the new window
        browser.switch_to_window(list(new_handle)[0])
        common.success("Switched to window '%s'" % list(new_handle)[0])
        common.info("Window title = '%s'" % browser.title)
        # close active (new) window using javascript
        browser.execute_script("close();")
        final_handles = set(browser.window_handles)
        if final_handles == start_handles:
            call_function = common.success
        else:
            common.info("Cannot close window '%s'" % browser.title)
            call_function = common.fail
        call_function("Closed window '%s'" % list(new_handle)[0])
        # switch back to the main window
        browser.switch_to_window(start_active_handle)
        common.success("Switched to main window '%s'" % start_active_handle)

    common.finish(function_result, "Checking multiple windows")
    return function_result

def test_function_Chrome(browser_Chrome):
    try:
        print()
        test_name = "Checking multiple windows operationing"
        test_start_time = time.time()
        common.startTest(test_name)

        overall_result = True
        overall_result = check_multi_windows(browser_Chrome) and overall_result
    except Exception as e:
        overall_result = False
        common.finish(False, "Exception detected (%s)" % e.__str__())
        raise e
    finally:
        common.finishTest(test_name, overall_result, test_start_time)
