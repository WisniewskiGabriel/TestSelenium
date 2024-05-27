import re
import time
from prefect import flow, task, variables
from browser_functions import login_acme, access_work_items_page, change_work_item_status


# Função principal que serve como entry point para o deployment posteriormente
@flow(name="Selenium with Prefect", log_prints=True)
def main_fn():
    driver = login_acme()  # Inicia o browser, loga no ACME System
    time.sleep(3)
    work_list = get_work_list()
    for work_id in work_list:
        driver = complete_work_item(driver, work_id, "Done by a bot.")
    driver.quit()  # Encerra instância do browser


@task(name="Get list of work-items IDs")
def get_work_list():
    str_list = variables.get("ids_to_close_acme")
    id_pattern = r"\d{8}"
    work_list = re.findall(id_pattern, str(str_list))
    return work_list


@flow(name="Complete Work-Item", log_prints=True)
def complete_work_item(driver, work_id, msg):
    driver = access_work_items_page(driver, work_id)  # Função que acessa o work-item de ID específico
    driver = change_work_item_status(driver, msg)
    return driver


if __name__ == "__main__":
    main_fn()
