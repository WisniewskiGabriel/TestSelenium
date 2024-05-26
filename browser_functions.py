from prefect import task, flow
from prefect.blocks.system import String
import re
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@task(name="Get URL for ACME System 1", log_prints=True)
def get_acme_url():
    url_acme_system1 = String.load("acme-system-url")
    pattern = r"(?<=value\=').+?(?='\)$)"
    url_acme_system1 = re.search(pattern, str(url_acme_system1)).group()

    return url_acme_system1


@task(name="Start browser at ACME")
def start_browser():
    url_acme_system1 = get_acme_url()
    driver = webdriver.Chrome()  # For Chrome
    driver.get(url_acme_system1)
    return driver


@task(name="Start login on ACME")
def login_acme():
    driver = start_browser()
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "To continue, please authenticate here"))
        )
        return True
    except TimeoutException:
        print("Timed out waiting for element to load")

    return driver
