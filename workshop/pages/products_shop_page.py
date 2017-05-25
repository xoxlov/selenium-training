from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class ProductsShopPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.count = 1

    def open_products_page(self):
        self.driver.get("http://localhost/litecart/en/rubber-ducks-c-1/")
        return self

    @property
    def product_list(self):
        # get all products on the page
        return self.driver.find_elements_by_css_selector(".product")

    @property
    def product_info(self, product_webelement):
        return product_webelement.find_element_by_css_selector(".info")

    @property
    def full_page_link(self):
        return self.driver.find_elements_by_css_selector("div#view-full-page a")

    def get_product_name(self, product_webelement):
        return product_webelement.find_element_by_css_selector(".info").get_property("innerText")

    def open_product_description(self, product):
        product.find_element_by_css_selector(".info").click()
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#view-full-page a")))

    def go_to_full_product_page(self, product):
        if (len(self.full_page_link)):
            self.full_page_link[0].click()
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name=add_cart_product]")))

    def find_product_page(self, product_to_buy):
        for product in self.product_list:
            if product_to_buy in self.get_product_name(product):
                self.open_product_description(product)
                self.go_to_full_product_page(product)
                return self
