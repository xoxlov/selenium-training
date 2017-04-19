import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    wait = WebDriverWait(driver, 10) # seconds

    login_field = driver.find_element_by_name("username")
    login_field.clear()
    login_field.send_keys("admin")

    password_field = driver.find_element_by_name("password")
    password_field.clear()
    password_field.send_keys("admin")

    driver.find_element_by_name("remember_me").click()

    driver.find_element_by_name("login").click()

    wait.until(EC.title_is("My Store"))
