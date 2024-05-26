from prefect import task, flow
from selenium import webdriver
from prefect.blocks.system import String
import re
import time
from browser_functions import login_acme
from selenium.webdriver.common.by import By


@flow(name="Selenium with Prefect", log_prints=True)
def main_fn():
    driver = login_acme()
    email_input = driver.find_element(By.ID("email"))
    email_input.send_keys("teste")
    # driver.quit()


if __name__ == "__main__":
    main_fn()
