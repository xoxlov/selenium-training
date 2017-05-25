from selenium import webdriver
from pages.products_shop_page import ProductsShopPage
from pages.products_details_page import ProductsDetailsPage
from pages.shopping_cart_page import ShoppingCartPage

class Application:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.products_shop_page = ProductsShopPage(self.driver)
        self.product_details_page = ProductsDetailsPage(self.driver)
        self.shopping_cart_page = ShoppingCartPage(self.driver)

    def quit(self):
        self.driver.quit()

    def add_products_to_card(self, products):
        for i in range(len(products)):
            self.products_shop_page.open_products_page()
            self.products_shop_page.find_product_page(products[i])
            self.product_details_page.add_product_to_cart()

    def clear_shopping_cart(self):
        self.shopping_cart_page.open()
        self.shopping_cart_page.clear_shopping_cart()
