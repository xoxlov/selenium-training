import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pprint

@pytest.fixture
def browser_Chrome(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd

@pytest.fixture
def browser_Ie(request):
    wd = webdriver.Ie()
    request.addfinalizer(wd.quit)
    return wd

@pytest.fixture
def browser_Firefox(request):
    ff_capabilities = DesiredCapabilities.FIREFOX
    ff_capabilities['marionette'] = False
    wd = webdriver.Firefox(capabilities=ff_capabilities)
    request.addfinalizer(wd.quit)
    return wd

def is_color_grey(rgba_color):
    values = [float(c) for c in (str.split(str(rgba_color[5:-1]), ", "))]
    return ((values[0] == values[1]) and (values[0] == values[2]))

def verify_price_color_grey(name, item):
    item_price_color = item.value_of_css_property("color")
    color_result = is_color_grey(item_price_color)
    result = "Passed" if (color_result) else "Failed"
    print("Color of %s price is grey: %s"  % (name, result))
    return color_result

def is_color_red(rgba_color):
    values = [float(c) for c in (str.split(str(rgba_color[5:-1]), ", "))]
    return ((values[1] == values[2]) and (values[1] == 0))

def verify_price_color_red(name, item):
    item_price_color = item.value_of_css_property("color")
    color_result = is_color_red(item_price_color)
    result = "Passed" if (color_result) else "Failed"
    print("Color of %s price is red: %s"  % (name, result))
    return color_result

def verify_style_striked_out(name, item):
    item_style = str.split(str(item.value_of_css_property("text-decoration")).lower())[0]
    style_result = (item_style == 'line-through')
    result = "Passed" if (style_result) else "Failed"
    print("Style of %s price is striked out: %s"  % (name, result))
    return style_result

def verify_style_bold(name, item):
    item_style = str(item.value_of_css_property("font-weight")).lower()
    # for Internet Explorer normal is 400, bold is 700
    style_result = (item_style == 'bold') or (item_style == '700')
    result = "Passed" if (style_result) else "Failed"
    print("Style of %s price is bold: %s (actual: '%s')"  % (name, result, item_style))
    return style_result

def verify_font_is_bigger(name1, item1, name2, item2):
    font_size_1 = float(str(item1.value_of_css_property("font-size")).lower()[:-2])
    font_size_2 = float(str(item2.value_of_css_property("font-size")).lower()[:-2])
    font_compare_result = (font_size_1 < font_size_2)
    result = "Passed" if (font_compare_result) else "Failed"
    print("Size of %s price is less than %s price: %s (%.2f ~ %.2f)"  % (name1, name2, result, font_size_1, font_size_2))
    return font_compare_result

def validate_goods(browser):
    check_result = ["Failed", "Passed"]
    function_result = True
    # get amount of tabs to go through
    browser.get("http://localhost/litecart/")
    tabs = browser.find_elements_by_css_selector("a[data-toggle='tab']")
    # go throught every tab and every item on it
    for tab in range(len(tabs)):
        browser.get("http://localhost/litecart/")
        tab_name = browser.find_elements_by_css_selector("a[data-toggle='tab']")[tab].get_attribute("innerText")
        print("\nChecking tab '%s'" % tab_name)
        browser.find_elements_by_css_selector("a[data-toggle='tab']")[tab].click()

        # products list, corresponds to the selected tab
        products_tab = browser.find_elements_by_css_selector(".tab-pane")[tab]
        # list goods displayed on the tab (in the products list)
        goods = products_tab.find_elements_by_css_selector("div.info")
        print("Found %s product(s)" % len(goods))

        for item in range(len(goods)):
            item_main_text = goods[item].find_element_by_css_selector("div.name").get_attribute("innerText")
            print("\nChecking product: %s" % item_main_text)
            if (len(goods[item].find_elements_by_css_selector(".regular-price"))):
                # get prices if there're as regular as campaign prices and verify color and style
                print("Regular and Action prices are present: Passed")
                elem_regular_price = goods[item].find_elements_by_css_selector(".regular-price")[0]
                item_regular_price = elem_regular_price.get_attribute("innerText")
                function_result = verify_price_color_grey("regular", elem_regular_price) and function_result
                function_result = verify_style_striked_out("regular", elem_regular_price) and function_result
                elem_campaign_price = goods[item].find_elements_by_css_selector(".campaign-price")[0]
                item_campaign_price = elem_campaign_price.get_attribute("innerText")
                function_result = verify_price_color_red("campaign", elem_campaign_price) and function_result
                function_result = verify_style_bold("campaign", elem_campaign_price) and function_result
                function_result = verify_font_is_bigger("regular", elem_regular_price,
                                                        "campaign", elem_campaign_price) and function_result
            else:
                # get prices if there's no campaign price, regular price presents only
                print("Regular and Action prices are missing: Passed")
                item_regular_price = goods[item].find_elements_by_css_selector(".price")[0].get_attribute("innerText")
                item_campaign_price = None
            goods[item].click()
            time.sleep(1)

            # proceed with detailed page
            item_detailed_text = browser.find_element_by_css_selector("h1.title").get_attribute("innerText")
            if (len(browser.find_elements_by_css_selector("div.featherlight-content"))):
                # look through popup window of detailed description and verify style and color
                if (len(browser.find_elements_by_css_selector("div.featherlight-content .regular-price"))):
                    elem_regular_price = browser.find_element_by_css_selector("div.featherlight-content .regular-price")
                    item_detailed_regular_price = elem_regular_price.get_attribute("innerText")
                    function_result = verify_price_color_grey("regular (detailed)", elem_regular_price) and function_result
                    function_result = verify_style_striked_out("regular (detailed)", elem_regular_price) and function_result
                    elem_campaign_price = browser.find_element_by_css_selector("div.featherlight-content .campaign-price")
                    item_detailed_campaign_price = elem_campaign_price.get_attribute("innerText")
                    function_result = verify_price_color_red("campaign (detailed)", elem_campaign_price) and function_result
                    function_result = verify_style_bold("campaign (detailed)", elem_campaign_price) and function_result
                    function_result = verify_font_is_bigger("regular (detailed)", elem_regular_price,
                                                            "campaign (detailed)", elem_campaign_price) and function_result
                else:
                    item_detailed_regular_price = browser.find_element_by_css_selector("div.featherlight-content .price").get_attribute("innerText")
                    item_detailed_campaign_price = None
            else:
                # look through whole page of detailed description and verify style and color
                if (len(browser.find_elements_by_css_selector(".regular-price"))):
                    elem_regular_price = browser.find_element_by_css_selector(".regular-price")
                    item_detailed_regular_price = elem_regular_price.get_attribute("innerText")
                    function_result = verify_price_color_grey("regular (detailed)", elem_regular_price) and function_result
                    function_result = verify_style_striked_out("regular (detailed)", elem_regular_price) and function_result
                    elem_campaign_price = browser.find_element_by_css_selector(".campaign-price")
                    item_detailed_campaign_price = elem_campaign_price.get_attribute("innerText")
                    function_result = verify_price_color_red("campaign (detailed)", elem_campaign_price) and function_result
                    function_result = verify_style_bold("campaign (detailed)", elem_campaign_price) and function_result
                    function_result = verify_font_is_bigger("regular (detailed)", elem_regular_price,
                                                            "campaign (detailed)", elem_campaign_price) and function_result
                else:
                    item_detailed_regular_price = browser.find_element_by_css_selector(".price").get_attribute("innerText")
                    item_detailed_campaign_price = None

            # verify product names on main and detailed pages
            function_result = (item_main_text == item_detailed_text) and function_result
            print("Product name is correct: %s (expected '%s' EQ actual '%s')" %
                 (check_result[(item_main_text == item_detailed_text)], item_main_text, item_detailed_text))
            function_result = (item_regular_price == item_detailed_regular_price) and function_result
            print("Product regular price is correct: %s (expected '%s' EQ actual '%s')" %
                  (check_result[(item_regular_price == item_detailed_regular_price)], item_regular_price, item_detailed_regular_price))

            # verify prices correctness if there's no campaign price, regular price presents only
            if (item_campaign_price and item_detailed_campaign_price):
                function_result = (item_campaign_price == item_detailed_campaign_price) and function_result
                print("Product campaign price is correct: %s (expected '%s' EQ actual '%s')" %
                      (check_result[(item_campaign_price == item_detailed_campaign_price)], item_campaign_price, item_detailed_campaign_price))
                function_result = (item_detailed_campaign_price < item_detailed_regular_price) and function_result
                print("Campaign price is greater than regular price: %s" %
                      (check_result[item_detailed_campaign_price < item_detailed_regular_price]))

            # most links cause pop-up frame, need to close it with 'X' button
            button_close = browser.find_elements_by_css_selector("div.featherlight.active .featherlight-close")
            if (len(button_close) > 0):
                button_close[0].click()
            else:
                browser.back()

    return function_result

def test_function_Firefox(browser_Firefox):
    print()
    browser_Firefox.get("http://localhost/litecart/")
    overall_result = True
    overall_result = validate_goods(browser_Firefox) and overall_result
    print("\n\nOverall result for FireFox: Passed" if overall_result else "Overall result: Failed")

def test_function_Ie(browser_Ie):
    print()
    browser_Ie.get("http://localhost/litecart/")
    overall_result = True
    overall_result = validate_goods(browser_Ie) and overall_result
    print("\n\nOverall result for Internet Explorer: Passed" if overall_result else "Overall result: Failed")

def test_function_Chrome(browser_Chrome):
    print()
    browser_Chrome.get("http://localhost/litecart/")
    overall_result = True
    overall_result = validate_goods(browser_Chrome) and overall_result
    print("\n\nOverall result for Chrome: Passed" if overall_result else "Overall result: Failed")
