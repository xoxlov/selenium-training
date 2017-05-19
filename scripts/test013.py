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

def process_shopping_cart(browser):
    common.start("Process shopping")
    function_result = True
    wait10 = WebDriverWait(browser, 10)

    items_to_buy = ["Yellow Duck", "Green Duck", "Purple Duck"]

    for i in range(3):
        browser.get("http://localhost/litecart/en/")
        wait10.until(EC.presence_of_element_located((By.LINK_TEXT, "Rubber Ducks")))
        common.success("Open main page")
        browser.find_elements_by_link_text("Rubber Ducks")[0].click()
        common.success("Open 'Rubber Ducks' sales page")
        time.sleep(5)

        product_list = browser.find_elements_by_css_selector(".product")
        for product in product_list:
            item = product.find_element_by_css_selector(".info")
            if (items_to_buy[i] in item.get_property("innerText")):
                common.success("Found product '%s'" % items_to_buy[i])
                item.click()
                wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#view-full-page a")))
                full_page_link_object = browser.find_elements_by_css_selector("div#view-full-page a")
                if (len(full_page_link_object)):
                    common.info("Popup window with desciption opened, looking for full page..")
                    full_page_link_object[0].click()
                common.success("Product '%s' page opened" % items_to_buy[i])

                common.info("Set parameters of the product to buy..")
                if (browser.find_elements_by_css_selector("select[name='options[Size]']")):
                    common_litecart.select_from_dropdown_list(browser,
                                                              {"location": "select[name='options[Size]']",
                                                               "value" : "Small", "description": "Small"})
                common_litecart.input_value_to_scrollable_field(browser, {"location": "input[name='quantity']", "value" : "1"})

                # save the text for the shopping cart dut to it contains price before product adding
                previous_amount = browser.find_element_by_css_selector(".quantity").get_property("innerText")
                previous_summ = browser.find_element_by_css_selector(".formatted_value").get_property("innerText")
                common.info("Shopping cart before operation contains %d products with summ = '%s'" % (int(previous_amount), previous_summ))
                browser.find_element_by_css_selector("button[name='add_cart_product']").click()
                # wait for the summ for shopping cart to be changed, i.e. previous text to disappear
                wait10.until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".quantity"), previous_amount))

                # check the data of the shopping cart
                operation_amount = browser.find_element_by_css_selector(".quantity").get_property("innerText")
                operation_summ = browser.find_element_by_css_selector(".formatted_value").get_property("innerText")
                common.info("Shopping cart after adding contains %d products with summ = '%s'" % (int(operation_amount), operation_summ))
                if (int(operation_amount) - 1) == int(previous_amount):
                    common.success("Product '%s' added to the Shopping Cart" % items_to_buy[i])
                else:
                    common.fail("Product '%s' added to the Shopping Cart" % items_to_buy[i])
                    function_result = False
                break  # break from loop [for product in product_list]

    # process Shopping Cart
    browser.find_element_by_css_selector("div#cart a").click()
    wait10.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-bordered")))
    common.success("Open Shopping Cart checkout page")

    items_to_remove = browser.find_elements_by_css_selector(".item")
    while (len(items_to_remove) > 1):
        # save total payment summ to watch for its change
        previous_payment_due = str.split(browser.find_element_by_css_selector(".table-bordered .footer").get_property("innerText"))[2]
        # get the name of the product to delete from shopping cart
        item_name = items_to_remove[1].find_element_by_css_selector("strong").get_property("innerText")
        common.info("Delete product '%s' from Shopping Cart.." % item_name)
        common.info("Payment summ before deleting of the product '%s' is: %s" % (item_name, previous_payment_due))
        remove_button = items_to_remove[1].find_element_by_css_selector("button[name=remove_cart_item]")
        remove_button.click()
        wait10.until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".table-bordered .footer"), previous_payment_due))
        if (len(browser.find_elements_by_css_selector(".table-bordered .footer"))):
            final_payment_due = str.split(browser.find_element_by_css_selector(".table-bordered .footer").get_property("innerText"))[2]
        else:
            final_payment_due = '$00.00 (There are no items in the cart)'
        common.info("Payment summ after deleting of the product '%s' is: %s" % (item_name, final_payment_due))
        common.success("Delete product '%s' from Shopping Cart" % item_name)
        items_to_remove = browser.find_elements_by_css_selector(".item")

    # Done: открыть главную страницу
    # Done: открыть первый товар из списка (Замечание: сделал по другому, ищу товар с заданным именем, а не какой попался первым)
    # Done: добавить первый товар в корзину (при этом может случайно добавиться товар, который там уже есть, ничего страшного)
    # Done: подождать, пока счётчик товаров в корзине обновится (Замечание: отслеживаю сумму для корзины, а не счётчик товаров)
    # Done: вернуться на главную страницу, повторить предыдущие шаги ещё два раза, чтобы в общей сложности в корзине было 3 единицы товара
    # Done: открыть корзину (в правом верхнем углу кликнуть по ссылке Checkout)
    # Done: удалить все товары из корзины один за другим, после каждого удаления подождать, пока внизу обновится таблица

    common.finish(function_result, "Processing to buy")
    return function_result

def test_function_Chrome(browser_Chrome):
    try:
        print()
        test_name = "Processing Shopping Cart"
        test_start_time = time.time()
        common.startTest(test_name)

        overall_result = True
        overall_result = process_shopping_cart(browser_Chrome) and overall_result
    except Exception as e:
        overall_result = False
        common.finish(False, "Exception detected (%s)" % e.__str__())
        raise e
    finally:
        common.finishTest(test_name, overall_result, test_start_time)
