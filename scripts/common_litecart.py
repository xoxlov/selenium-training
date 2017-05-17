import time
import common

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

def do_login_admin(browser):
    common.info("Processing login..")
    function_result = True
    # go to the admin login page and wait for page to be loaded
    browser.get("http://localhost/litecart/admin/")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[value=Login]")))
    # enter credentials
    login_field = browser.find_element_by_name("username")
    login_field.clear()
    login_field.send_keys("admin")
    password_field = browser.find_element_by_name("password")
    password_field.clear()
    password_field.send_keys("admin")
    # press [Login] button and wait for next page to be loaded
    browser.find_element_by_css_selector('button[name="login"]').click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li#widget-discussions")))
    if (browser.find_element_by_css_selector("li#widget-discussions")):
        function_result = True
        common.success("Login successful")
    else:
        function_result = False
        common.fail("Cannot login to admin page")
    return function_result


def input_value_to_input_field(browser, data_to_set):
    value_to_set = data_to_set["value"]
    field_to_be_set = browser.find_element_by_css_selector(data_to_set["location"])
    field_to_be_set.clear()
    field_to_be_set.send_keys(value_to_set)
    if (field_to_be_set.get_property("value") == value_to_set):
        common.info("Set %s = '%s': ok" % (data_to_set["location"], value_to_set))
        return True
    return False

def select_from_dropdown_list(browser, data_to_set):
    value_to_set = data_to_set["value"]
    # if no value should be set then just return
    if (not value_to_set):
        return True
    field_to_be_set = browser.find_element_by_css_selector(data_to_set["location"])
    select_field = Select(field_to_be_set)
    try:
        WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, data_to_set["location"])))
        select_field.select_by_value(value_to_set)
        if (field_to_be_set.get_property("value") == value_to_set):
            common.info("Set %s = '%s': ok" % (data_to_set["location"], data_to_set["description"]))
        return True
    except:
        common.fail("Set %s = '%s'" % (data_to_set["location"], data_to_set["description"]))
        return False

def input_value_to_scrollable_field(browser, data_to_set): #{"location": "", "value": ""})
    value_to_set = data_to_set["value"]
    field_to_be_set = browser.find_element_by_css_selector(data_to_set["location"])
    field_to_be_set.clear()
    field_to_be_set.send_keys(value_to_set)
    # TODO: нужна проверка установленного значения
    common.info("Set %s = '%s': ok" % (data_to_set["location"], value_to_set))
    return True

def set_checkbox(browser, locator, checked=True):
    elem = browser.find_element_by_css_selector(locator)
    if elem.get_property("checked") != checked:
        elem.click()
    common.info("Set %s = '%s': ok" % (locator, "Checked" if checked else "Not checked"))
    return True
