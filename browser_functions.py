from Tools.scripts.var_access_benchmark import B
from prefect import task, get_run_logger
from prefect.blocks.system import String
import re
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


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
    is_header_loaded = False
    header_text = "To continue, please authenticate here"

    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//h3[contains(text(), "' + header_text + '")]'))
        )
        is_header_loaded = True
    except TimeoutException:
        is_header_loaded = False
    finally:
        if is_header_loaded:
            print("Login page is loaded")
        else:
            get_run_logger().error("Page not loaded yet.")


