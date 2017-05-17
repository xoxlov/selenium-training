import pytest
import time
import random
import string

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from elizabeth import Personal
from elizabeth import Address

import common

@pytest.fixture
def browser_Chrome(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

def get_user_data(test_locale='en'):
    person = {}
    user = Personal(test_locale)
    address = Address(test_locale)

    person['first_name'], person['last_name'] = user.full_name(gender='male').split()
    common.success("Generated user name '%s %s'" % (person['first_name'], person['last_name']))
    person['email'] = user.email(gender='male')
    common.success("Generated email '%s'" % person['email'])
    person['street'] = address.address()
    person['city'] = address.city()
    person['state'] = address.state()
    person['postcode'] = address.postal_code()
    common.success("Generated address '%s %s, %s, %s'" % (person['postcode'], person['state'], person['city'], person['street']))
    person['password'] = ''.join(random.SystemRandom().choice(string.digits + string.ascii_letters) for _ in range(10))
    common.success("Generated password '%s'" % person['password'])
    if (test_locale == 'en'):
        person['country_code'] = 'US'
        person['country'] = 'United States'
        person['state_code'] = 'IA'
        person['state'] = 'Iowa'
    elif (test_locale == 'ru'):
        person['country_code'] = 'RU'
        person['country'] = 'Russian Federation'
        person['state_code'] = None
        person['state'] = None
    else:
        person['country_code'] = None
        person['country'] = None
        person['state_code'] = None
        person['state'] = None
    common.success("Generated country '%s' and state '%s'" % (person['country'], person['state']))
    return person

def input_value_to_input_field(browser, data_to_set):
    value_to_set = data_to_set["value"]
    field_to_be_set = browser.find_element_by_css_selector(data_to_set["location"])
    field_to_be_set.clear()
    field_to_be_set.send_keys(value_to_set)
    if (field_to_be_set.get_property("value") == value_to_set):
        common.info("Set %s = '%s': ok" % (data_to_set["location"], value_to_set))
        return True
    return False

def set_check_box(browser, locator, set=True):
    field_to_be_set = browser.find_element_by_css_selector(locator)
    try:
        if (field_to_be_set.get_property("checked") != set):
            field_to_be_set.click()
        return True
    except:
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

def register_user(browser):
    common.start("Starting registration")
    function_result = True

    browser.get("http://www.localhost/litecart/")
    browser.find_element_by_link_text("New customers click here").click()
    common.success("Get to the registration page")

    user = get_user_data('en')
    # set registration data
    registration_data = [
        {"location": "input[name=firstname]", "value": user["first_name"] },
        {"location": "input[name=lastname]", "value": user["last_name"] },
        {"location": "input[name=address1", "value": user["street"] },
        {"location": "input[name=city]", "value": user["city"] },
        {"location": "#box-create-account input[name=email]", "value": user["email"] },
        {"location": "#box-create-account input[name=password]", "value": user["password"] },
        {"location": "input[name=confirmed_password]", "value": user["password"] },
        {"location": "input[name=postcode]", "value": user["postcode"] }
    ]
    for field in registration_data:
        function_result = input_value_to_input_field(browser, field) and function_result
    # select country and state from dropdown list
    registration_data = [
        {"location": "select[name=country_code]", "value": user["country_code"], "description": user["country"] },
        {"location": "select[name=zone_code]", "value": user["state_code"], "description": user["state"] }
    ]
    for field in registration_data:
        function_result = select_from_dropdown_list(browser, field) and function_result
    # unsubscribe from newsletters
    function_result = set_check_box(browser, "input[name=newsletter]", False) and function_result
    common.info("Uncheck '%s' to unsubscribe from newsletters: ok" % "input[name=newsletter]")
    # click registration button
    browser.find_element_by_css_selector("button[name=create_account]").click()
    common.success("Login successfull")
    # make logout with first appropriate link
    browser.find_element_by_link_text("Logout").click()
    common.success("Logout successfull")
    # make login back using left form
    registration_data = [
        {"location": "#box-account-login input[name=email]", "value": user["email"] },
        {"location": "#box-account-login input[name=password]", "value": user["password"] }
    ]
    for field in registration_data:
        function_result = input_value_to_input_field(browser, field) and function_result
    browser.find_element_by_css_selector("button[name=login]").click()
    common.success("Second login successfull")
    # make logout again to get out of store
    browser.find_element_by_link_text("Logout").click()
    common.success("Logout successfull")

    common.finish(function_result, "Registration")
    return function_result


def test_function_Chrome(browser_Chrome):
    try:
        print()
        test_name = "User registration"
        test_start_time = time.time()
        common.startTest(test_name)

        overall_result = True
        overall_result = register_user(browser_Chrome) and overall_result
    except Exception as e:
        overall_result = False
        common.finish("Exception detected")
        raise e
    finally:
        common.finishTest(test_name, overall_result, test_start_time)
