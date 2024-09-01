import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .wdriver import driver
from .wdriver import PAS, USER


# login
def login(driver=driver):
    email = driver.find_element(by=By.ID, value='email')
    passw = driver.find_element(by=By.ID, value='component-outlined')
    btn_Sing = driver.find_element(by=By.ID, value="signInButton")

    # escribir pas y user
    email.send_keys(USER)  # Ingresa texto en el cuadro de texto
    passw.send_keys(PAS)
    time.sleep(3)  # 2 segundos
    btn_Sing.click()
    time.sleep(5)

    # driver.refresh()


# ir a programa
def get_element_click_newPage(driver=driver, css_selector: str = "li[itemid='calendar']"):
    try:
        # Espera a que el elemento sea clicable (visible y habilitado)
        element = WebDriverWait(driver, 14).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        element.click()
    except Exception as e:
        print(f"Error al intentar hacer clic en el elemento: {e}")


def close_popup_with_js(driver, css_selector: str = None):
    try:
        # Espera a que el botón "Not now" (o "ui-close") sea clicable
        close_button = WebDriverWait(driver, 14).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".installPwaBox .ui-close"))
        )
        close_button.click()
    except Exception as e:
        print(f"Error al intentar cerrar el popup: {e}")
