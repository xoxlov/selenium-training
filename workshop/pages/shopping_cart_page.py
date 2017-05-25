from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ShoppingCartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.count = 1

    def open(self):
        self.driver.get("http://localhost/litecart/en/checkout")
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".table-bordered")))
        return self

    @property
    def items_to_remove(self):
        return self.driver.find_elements_by_css_selector(".item")

    @property
    def remove_buttons(self):
        return self.driver.find_elements_by_css_selector(".item button[name=remove_cart_item]")

    @property
    def products_to_buy_table(self):
        return self.driver.find_elements_by_css_selector(".table-bordered .footer")

    def get_element_text(self, webelement):
        return webelement.get_property("innerText")

    def get_total_payment_summ(self):
        if self.products_to_buy_table:
            return str.split(self.get_element_text(self.products_to_buy_table[0]))[2]
        return "$0.00 (There are no items in the cart)"

    def clear_shopping_cart(self):
        while self.items_to_remove:
            previous_payment_due = self.get_total_payment_summ()
            self.remove_buttons[0].click()
            self.wait.until_not(EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".table-bordered .footer"), previous_payment_due))
