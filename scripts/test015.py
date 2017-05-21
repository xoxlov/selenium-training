import pytest
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import common
import common_litecart

@pytest.fixture
def browser_Chrome(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def check_log(browser):
    browser_log_types = browser.log_types
    for type in browser_log_types:
        current_log = browser.get_log(type)
        length = len(current_log)
        if (length):
            common.fail("---- There is something in the log '%s'" % type)
            common.info("     records amount: %d" % length)
            for i in range(length):
                common.info("%3d: %s" % (i, current_log[i]))
            return False
        else:
            common.success("---- Log '%s' is empty" % type)
    return True

def browse_catalog(browser):
    common.start("Start browsing catalog")
    function_result = True
    common_litecart.do_login_admin(browser)
    wait10 = WebDriverWait(browser, 10)

    # go to the 'Catalog' page
    browser.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".data-table")))
    length = len(browser.find_elements_by_css_selector("tbody tr"))

    for i in range(1, length):
        common.info("")
        # go to the 'Catalog' page
        browser.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
        wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".data-table")))
        common.success("Open 'Catalog' page")
        check_log(browser)

        table_lines = browser.find_elements_by_css_selector("tbody tr")
        category = table_lines[i].find_elements_by_css_selector("input")[0].get_property("name")
        if "products" in category:
            product = table_lines[i].find_elements_by_css_selector("a")[0]
            product_name = product.get_property("innerText")
            common.info("Process product '%s'" % product_name)
            product.click()
            wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name=delete]")))
            common.success("Process product '%s'" % product_name)
            # Замечание:  если раскомментировать эту строку, то получим замечание в логе драйвера и аварийный останов теста,
            #             но эта строка использовалась для просмотра, что лог доступен и можно вывести его сообщения
            #browser.execute_script("alert('OK');")
            check_log(browser)

    # Done: зайти в админскую часть
    # Done: открыть каталог, категорию, которая содержит товары
    # Done: последовательно открывать страницы товаров
    # Done: проверять, не появляются ли в логе браузера сообщения (любого уровня)
    common.finish(function_result, "Browse catalog")
    return function_result

def test_function_Chrome(browser_Chrome):
    try:
        print()
        test_name = "Browser log access check"
        test_start_time = time.time()
        common.startTest(test_name)

        overall_result = True
        overall_result = browse_catalog(browser_Chrome) and overall_result
    except Exception as e:
        overall_result = False
        common.finish(False, "Exception detected")
        raise e
    finally:
        common.finishTest(test_name, overall_result, test_start_time)
