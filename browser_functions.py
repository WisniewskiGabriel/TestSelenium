import re
import time

from prefect import task, flow, get_run_logger
from prefect.blocks.system import Secret
from prefect.blocks.system import String
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


@task(name="Get URL for ACME System 1", log_prints=True)  # Pegar bloco que contem URL base do ACME
def get_acme_url():
    url_acme_system1 = String.load("acme-system-url")
    pattern = r"(?<=value\=').+?(?='\)$)"
    url_acme_system1 = re.search(pattern, str(url_acme_system1)).group()

    return url_acme_system1


@task(name="Start browser at ACME", log_prints=True)  # Inicia o browser no URL do ACME
def start_browser():
    url_acme_system1 = get_acme_url()
    driver = webdriver.Chrome()  # For Chrome
    driver.get(url_acme_system1)
    return driver


@task(name="Get ACME credentials", log_prints=True)  # Monta classe de credencial do ACME
def get_acme_credentials():
    #  Padrões de RegEx para capturar valores dos Blocks
    email_pattern = r"(?<=id\:).+?(?=\|)"  # Padrão para pegar e-mail
    next_block_pattern = r"(?<=secret_block:).+?(?='\)$)"  # Padrão para pegar nome do próx. bloco (Secret)

    # Leitura do primeiro block
    block_str = String.load("credential-for-acme-system1")

    # Captura dos valores dos blocks
    user = re.search(email_pattern, str(block_str)).group()  # Leitura por RegEx do ID do user
    name_of_next_block = re.search(next_block_pattern,
                                   str(block_str)).group()  # Leitura por RegEx do nome do próx. block que contém o Secret
    password = Secret.load(name_of_next_block).get()  # Captura da senha via Secret Block

    class UserCredentials:
        def __init__(self):
            self.user = user
            self.password = password

    credentials = UserCredentials()

    return credentials


@flow(name="Start login on ACME", log_prints=True)
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

    credentials = get_acme_credentials()
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/form/button")

    email_input.send_keys(str(credentials.user))
    password_input.send_keys(str(credentials.password))
    login_button.click()

    driver.get(get_acme_url())

    return driver


@task(name="Get Work-Items page", log_prints=True)
def access_work_items_page(driver, id_work_item):
    url_of_work_item = str(get_acme_url()) + "work-items/" + id_work_item
    print("Going to URL: " + url_of_work_item)
    driver.get(url_of_work_item)
    time.sleep(0.5)
    return driver
