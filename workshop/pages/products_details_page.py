from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class ProductsDetailsPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @property
    def cart_items_count(self):
        return self.driver.find_element_by_css_selector(".quantity")

    @property
    def cart_total_summ(self):
        return self.driver.find_element_by_css_selector(".formatted_value")

    @property
    def size_scroll_list(self):
        size_selector = "select[name='options[Size]'"
        if (self.driver.find_elements_by_css_selector(size_selector)):
            return self.driver.find_element_by_css_selector(size_selector)
        return None

    @property
    def add_to_cart_button(self):
        return self.driver.find_element_by_css_selector("button[name='add_cart_product']")

    def select_size(self, value_to_set):
        if (self.size_scroll_list):
            select_field = Select(self.size_scroll_list)
            select_field.select_by_value(value_to_set)

    def input_quantity(self, value_to_set):
        field_to_be_set = self.driver.find_element_by_css_selector("input[name='quantity']")
        field_to_be_set.clear()
        field_to_be_set.send_keys(value_to_set)

    def add_product_to_cart(self):
        self.select_size("Small")
        self.input_quantity(1)
        initial_amount = self.cart_items_count.get_property("innerText")
        self.add_to_cart_button.click()
        # wait for the summ for shopping cart to be changed, i.e. previous text to disappear
        self.wait.until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".quantity"), initial_amount))
