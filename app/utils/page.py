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
    nav_prog = WebDriverWait(driver, 14).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    print(nav_prog)
    nav_prog.click()
    time.sleep(2)
    # driver.refresh()
    # btn_programacion = driver.find_element(By.CLASS_NAME, "ui-calendar selected")
    # print(nav_prog)
