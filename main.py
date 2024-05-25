from prefect import task, flow
from selenium import webdriver
from prefect.blocks.system import String
import re
import time


@task(name="Get URL for ACME System 1", log_prints=True)
def get_acme_url():
    url_acme_system1 = String.load("acme-system-url")
    pattern = r"(?<=value\=').+?(?='\)$)"
    url_acme_system1 = re.search(pattern, str(url_acme_system1)).group()

    return url_acme_system1


@flow(name="Selenium with Prefect", log_prints=True)
def main_fn():
    url_acme_system1 = get_acme_url()
    chrome_driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome()  # For Chrome
    driver.get(url_acme_system1)
    time.sleep(5)


if __name__ == "__main__":
    main_fn()
