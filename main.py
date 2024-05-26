import time
from prefect import flow
from browser_functions import login_acme, access_work_items_page


@flow(name="Selenium with Prefect", log_prints=True)
def main_fn():
    driver = login_acme()
    time.sleep(3)
    driver = access_work_items_page(driver, "98687053")
    time.sleep(3)
    driver.quit()


if __name__ == "__main__":
    main_fn()
