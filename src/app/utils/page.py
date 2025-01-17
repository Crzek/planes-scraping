import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .wdriver import CustomChromeDriver
from globals import PAS, USER

"""
se encarga de la navegacion en la pagina

"""

# login


def login_page(driver: CustomChromeDriver):
    email = driver.find_element(by=By.ID, value='email')
    passw = driver.find_element(by=By.ID, value='component-outlined')
    btn_Sing = driver.find_element(by=By.ID, value="signInButton")

    # escribir pas y user
    email.send_keys(USER)  # Ingresa texto en el cuadro de texto
    passw.send_keys(PAS)
    time.sleep(2)  # 2 segundos
    btn_Sing.click()
    # time.sleep(5)

    # driver.refresh()


# ir a programa
def get_element_click_newPage(driver, css_selector: str = "li[itemid='calendar']", xpath: str = None):
    """
    Clicks on an element in a web page using the given CSS selector or XPath.

    Args:
        driver: The WebDriver instance.
        css_selector (str, optional): The CSS selector of the element to click. Defaults to "li[itemid='calendar']".
        xpath (str, optional): The XPath of the element to click. Defaults to None.

    Raises:
        Exception: If an error occurs while trying to click on the element.

    """

    try:
        # Espera a que el elemento sea clicable (visible y habilitado)
        if xpath is not None:
            element = WebDriverWait(driver, 14).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        else:
            element = WebDriverWait(driver, 14).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )

        element.click()
    except Exception as e:
        print(f"Error al intentar hacer clic en el elemento: {e}")


def close_popup_with_js(driver, css_selector: str = None):
    try:
        # Espera a que el botón "Not now" (o "ui-close") sea clicable
        close_button = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".installPwaBox .ui-close"))
        )
        close_button.click()
    except Exception as e:
        print(f"Error al intentar cerrar el popup: {e}")
