import time
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC

import pprint

@pytest.fixture
def driver(request):
    driver = run_firefox(request)
    #driver = run_firefox_45jsr(request)
    #request.addfinalizer(driver.quit)
    return driver

@pytest.fixture
def run_chrome(request):
    browser = webdriver.Chrome()
    #request.addfinalizer(browser.quit)
    return browser

@pytest.fixture
def run_firefox(request):
    browser = webdriver.Firefox()
    #request.addfinalizer(browser.quit)
    return browser

@pytest.fixture
def run_firefox_45jsr(request):
    firefox_capabilities = DesiredCapabilities.FIREFOX
    #firefox_capabilities['binary'] = 'c:\Program Files (x86)\Mozilla Firefox 45esr\'
    firefox_capabilities['marionette'] = False
    #browser = webdriver.Firefox(firefox_binary='c:\\Program Files (x86)\\Mozilla Firefox 45esr\\')
    browser = webdriver.Firefox
    return browser

def run_ie(request):
    browser = webdriver.Ie()
    #request.addfinalizer(browser.quit)
    return browser

def test_example(driver):
    driver.get("http://localhost/litecart/admin/")
    pprint.pprint(driver.capabilities)
    wait = WebDriverWait(driver, 10) # seconds
