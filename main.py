import time
from prefect import flow
from browser_functions import login_acme, access_work_items_page


# Função principal que serve como entry point para o deployment posteriormente
@flow(name="Selenium with Prefect", log_prints=True)
def main_fn():
    driver = login_acme() # Inicia o browser, loga no ACME System
    time.sleep(3)
    driver = access_work_items_page(driver, "98687053") # Função que acessa o work-item de ID específico
    time.sleep(3)
    driver.quit() # Encerra instância do browser


if __name__ == "__main__":
    main_fn()
