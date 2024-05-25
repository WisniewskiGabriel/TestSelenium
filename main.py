from prefect import task, flow
from selenium import webdriver
from prefect.blocks.system import String
import re
import time
from browser_functions import get_acme_url, start_browser


@flow(name="Selenium with Prefect", log_prints=True)
def main_fn():
    driver = start_browser()
    driver.get("https://google.com")
    time.sleep(4)


if __name__ == "__main__":
    main_fn()
