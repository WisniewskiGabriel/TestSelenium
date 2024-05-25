from prefect import task, flow
from prefect.blocks.system import String
import re
from selenium import webdriver


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
