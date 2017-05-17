import pytest
import time
import random
import string
import os

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

def add_new_goods(browser):
    common.start("Start add new goods")
    function_result = True
    common_litecart.do_login_admin(browser)

    wait = WebDriverWait(browser, 10)
    # go to the 'Add New Product' page
    browser.find_element_by_link_text("Catalog").click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.pull-right")))
    common.success("Open 'Add New Product' page")
    browser.find_elements_by_css_selector("ul.pull-right a")[1].click()
    common.success("Open 'General' tab")

    # fill the data on the 'General' tab
    # Status
    browser.execute_script("arguments[0].click();", browser.find_element_by_css_selector("input[name=status][value='1']"))
    #browser.execute_script("document.querySelector(\"input[name=status][value='1']\").click()")
    common.info("Set %s = '%s': ok" % ("input[name=status]", "Enabled"))
    # Categories
    common_litecart.set_checkbox(browser, "input[name='categories[]'][value='0']", True)
    common_litecart.set_checkbox(browser, "input[name='categories[]'][value='1']", True)
    # Default category -- skipped
    # Product Groups
    common_litecart.set_checkbox(browser, "input[name='product_groups[]'][value='1-1']", False)
    common_litecart.set_checkbox(browser, "input[name='product_groups[]'][value='1-2']", False)
    common_litecart.set_checkbox(browser, "input[name='product_groups[]'][value='1-3']", True)
    # Date Valid From
    browser.find_element_by_css_selector("input[name=date_valid_from]").send_keys("01.05.2017")
    common.info("Set %s = '%s': ok" % ("input[name=date_valid_from]", "01.05.2017"))
    # Date Valid To
    browser.find_element_by_css_selector("input[name=date_valid_to]").send_keys("01.09.2017")
    common.info("Set %s = '%s': ok" % ("input[name=date_valid_to]", "01.09.2017"))

    # Code
    common_litecart.input_value_to_input_field(browser, {"location":"input[name=code]", "value":"fd001"})
    # Name
    common_litecart.input_value_to_input_field(browser, {"location":"input[name='name[en]']", "value":"Fried Duck"})
    # SKU
    common_litecart.input_value_to_input_field(browser, {"location":"input[name=sku]", "value":"FD001"})
    # GTIN -- skipped
    # TARIC -- skipped
    # Quantity
    common_litecart.input_value_to_input_field(browser, {"location":"input[name=quantity]", "value":70})
    common_litecart.select_from_dropdown_list(browser, {"location": "select[name=quantity_unit_id]", "value" : "1", "description": "pcs"})
    # Weight
    common_litecart.input_value_to_scrollable_field(browser, {"location": "input[name=weight]", "value": "4.5"})
    common_litecart.select_from_dropdown_list(browser, {"location": "select[name=weight_class]", "value": "lb", "description": "lb"})
    # Width x Height x Length
    common_litecart.input_value_to_scrollable_field(browser, {"location": "input[name=dim_x]", "value": "20,0"})
    common_litecart.input_value_to_scrollable_field(browser, {"location": "input[name=dim_y]", "value": "30,0"})
    common_litecart.input_value_to_scrollable_field(browser, {"location": "input[name=dim_z]", "value": "40,0"})
    common_litecart.select_from_dropdown_list(browser, {"location": "select[name=dim_class]", "value": "cm", "description": "cm"})
    # Delivery Status
    common_litecart.select_from_dropdown_list(browser, {"location": "select[name=delivery_status_id]", "value": "1", "description": "3-5 days"})
    # Sold Out Status
    common_litecart.select_from_dropdown_list(browser, {"location": "select[name=sold_out_status_id]", "value": "1", "description": "Sold out"})
    # Images
    common_litecart.input_value_to_input_field(browser,
                                               {"location": "input[name='new_images[]']", "value": os.getcwd() + "\\images\\fried_duck.jpg"})
    common.info("Set %s = '%s': ok" % ("input[name='new_images[]']", os.getcwd() + "\\images\\fried_duck.jpg"))

    # go to the 'Information' tab
    browser.find_element_by_css_selector("a[href='#tab-information']").click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='meta_description[en]']")))
    common.success("Open 'Information' tab")
    # fill the data on the 'Information' tab
    # Manufacturer
    common_litecart.select_from_dropdown_list(browser, {"location": "select[name=manufacturer_id]", "value": "1", "description": "ACME Corp."})
    # Supplier -- skipped
    # Keywords
    common_litecart.input_value_to_input_field(browser, {"location": "input[name=keywords]", "value": "fried duck food"})
    # Short Description
    common_litecart.input_value_to_input_field(browser, {"location": "input[name='short_description[en]']", "value": "short description"})
    # Description
    common_litecart.input_value_to_input_field(browser, {"location": "textarea[name='description[en]']",
                                                         "value": "Full description of the fried duck"})
    # Attributes -- skipped
    # Head Title -- skipped
    # Meta Description -- skipped

    # go to the 'Prices' tab
    browser.find_element_by_css_selector("a[href='#tab-prices']").click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='gross_prices[EUR]']")))
    common.success("Open 'Prices' tab")
    # fill the data on the 'Prices' tab
    # Purchase Price
    common_litecart.input_value_to_scrollable_field(browser, {"location": "input[name=purchase_price]", "value": "25"})
    common_litecart.select_from_dropdown_list(browser, {"location": "select[name=purchase_price_currency_code]",
                                                        "value": "USD", "description": "US Dollars"})
    # Tax Class -- skipped
    # Price
    common_litecart.input_value_to_input_field(browser, {"location": "input[name='prices[USD]']", "value": "25"})
    # Price Incl. Tax -- skipped

    # press 'SAVE' button
    browser.find_element_by_css_selector("button[name=save]").click()

    # go to the main store page, tab 'NEW' and check if new goods are there
    browser.get("http://localhost/litecart/")
    browser.find_element_by_css_selector("a[href='#latest-products']").click()
    if (browser.find_elements_by_css_selector("a[title='Fried Duck']")):
        common.success("Found new item in the store")

    common.finish(function_result, "Add new goods")
    return function_result

def test_function_Chrome(browser_Chrome):
    try:
        print()
        test_name = "Add new goods"
        test_start_time = time.time()
        common.startTest(test_name)

        overall_result = True
        overall_result = add_new_goods(browser_Chrome) and overall_result
    except Exception as e:
        overall_result = False
        common.finish(False, "Exception detected")
        raise e
    finally:
        common.finishTest(test_name, overall_result, test_start_time)
