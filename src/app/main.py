#!/usr/bin/env python
# coding: utf-8

# In[33]
import time
import datetime

from bs4 import BeautifulSoup

from src.app.utils.utils import clas_to_series
from src.app.utils.wdriver import CustomChromeDriver

from src.app.utils.page import login_page, get_element_click_newPage, close_popup_with_js
from src.app.utils.utils import save_Book_by_tag

# logging que esta el modulo (__init__.py)
from . import logger


def navigate_to_programming(today: bool = False, sleep: int = 2, driver: CustomChromeDriver = None):
    """
    Navigates to the programming page.

    Args:
        today (bool, optional): Flag indicating whether to navigate to today's programming. Defaults to False.
        sleep (int, optional): Number of seconds to sleep before continuing. Defaults to 2.
    """

    # eliminar wrapper
    close_popup_with_js(driver, ".wrapper .ui-close")

    # navegar a programacion, icono program
    print("navegar a programacion")
    get_element_click_newPage(
        driver, xpath="/html/body/div[2]/div[1]/div/div[3]/ul/li[5]")

    show_filtro(driver)

    time.sleep(sleep)
    if not today:
        # Sigiente dia
        # <span class="datebtn ui-after"></span>
        get_element_click_newPage(driver, "span.ui-after")
        logger.info("siguiente dia")


def config_hour_navigate(driver: CustomChromeDriver):
    """
    Configura la hora local en la navegacion.

    Args:
        driver (CustomChromeDriver): Driver de selenium.
    """
    # abrir navegacion
    get_element_click_newPage(driver, "#menuButtonOpen")
    # abrir configuracion
    get_element_click_newPage(
        driver, xpath="/html/body/div[2]/div[5]/div[2]/ul[2]/li[2]")

    # Seccion -> config General
    get_element_click_newPage(
        driver, xpath="/html/body/div[4]/div[3]/div/div[2]/div[1]/div/div[2]/div/div")
    get_element_click_newPage(
        driver, xpath="/html/body/div[5]/div[3]/ul/li[1]")
    # END Seccion -> config General

    # Seccion -> config programacion
    get_element_click_newPage(
        driver, xpath="/html/body/div[4]/div[3]/div/div[2]/header/div/div[2]/div/button[3]/span[1]")

    time.sleep(1)
    # abrir input desplagable
    get_element_click_newPage(
        driver, xpath="/html/body/div[4]/div[3]/div/div[2]/div[1]/div/div[1]/div/div")

    # seleccionar hora local
    get_element_click_newPage(
        driver, xpath="/html/body/div[5]/div[3]/ul/li[1]")

    time.sleep(1)
    # aceptar config
    get_element_click_newPage(
        driver, xpath="/html/body/div[4]/div[3]/div/div[2]/div[2]/div[1]/button")
    logger.info("configuracion de hora local")


def logout(driver: CustomChromeDriver):
    # abrir navegacion
    get_element_click_newPage(driver, "#menuButtonOpen")

    # desconectar
    get_element_click_newPage(
        driver, xpath="/html/body/div[2]/div[5]/div[2]/ul[3]/li[2]")


def navigate_in_filter(driver, time_sl: int = 4):
    time.sleep(time_sl)
    # Seleccionar todos los filtros
    get_element_click_newPage(
        driver, xpath="/html/body/div[7]/div[3]/div/div[2]/div[5]/div[1]/div/label")
    # desceleccionar Canceled
    get_element_click_newPage(
        driver, xpath="/html/body/div[7]/div[3]/div/div[2]/div[5]/div[2]/div[15]/label"
    )
    # desceleccionar Maintenance
    get_element_click_newPage(
        driver, xpath="/html/body/div[7]/div[3]/div/div[2]/div[5]/div[2]/div[16]/label"
    )
    # desceleccionar not avialable
    get_element_click_newPage(
        driver, xpath="/html/body/div[7]/div[3]/div/div[2]/div[5]/div[2]/div[17]/label"
    )
    # desceleccionar type rating
    get_element_click_newPage(
        driver, xpath="/html/body/div[7]/div[3]/div/div[2]/div[5]/div[2]/div[5]/label"
    )

    time.sleep(time_sl+2)
    # aceptar config
    get_element_click_newPage(
        driver, xpath="/html/body/div[7]/div[3]/div/div[3]/div[1]/button")


def show_filtro(driver, time_sl: int = 4):
    # ir a filtro
    time.sleep(time_sl-2)
    get_element_click_newPage(driver, "i.ui-filters")
    logger.info("click filtro")

    navigate_in_filter(driver, time_sl)


def tag_find_by_attr(list_tag: list, attr_tag: str, value: str = None):
    """
    find tag by attribute and value

    input: list_tag, attr, value
    return : attributes values
    """
    list_vales = []
    for tag in list_tag:
        value = tag.attrs[attr_tag]
        list_vales.append(value)
    return list_vales


def stract_info_from_tag(list_info: list[str]):
    """
    stract info de un string
    """
    for info in list_info:
        if "DUAL" in info or "PIC" in info:
            # incargado de guardar la reserva
            saved: bool = save_Book_by_tag(info)
            # print(info + "\n")


def delete_parts(soup: BeautifulSoup):

    h1_simuladores = soup.find(
        'h1', string=lambda text: text and text.strip().lower() == "simuladores")

    # Eliminar desde el elemento encontrado hasta el final
    if h1_simuladores:
        # Obtener todos los elementos posteriores a `h2_simuladores` en el árbol
        for sibling in h1_simuladores.find_all_next():
            sibling.extract()  # Eliminar cada elemento

        # Eliminar también el propio elemento h2_simuladores si es necesario
        h1_simuladores.decompose()

    return soup


def main(
        today: bool = False,
        hidden: bool = False,
        architecture: str = "arm64",
        to_pdf: bool = False,
        date: datetime.date = None):
    # from src.app.utils.wdriver import driver  # nopep8
    try:
        driver = CustomChromeDriver(
            hidden_windows=hidden,
            # architecture=architecture
        )
        login_page(driver)

        # # Configurar la hora local
        # config_hour_navigate(driver)

        # # desloagaer y volver a logear
        # logout(driver)
        # time.sleep(2)
        # login_page(driver)

        # toda la navegacion comienza aqui en esta funcion
        navigate_to_programming(today, driver=driver)

        # Cargar los datos
        time.sleep(6)
        logger.info("Cargando los datos...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Eliminar partes innecesarias
        delete_parts(soup)

        # titulo de la pagina (dia, mes, año)
        title_day = soup.find("span", class_="date").get_text()

        # obtener solo vuelos
        booking = soup.select(".BookingContainer_wrapper__VpZwN")
        logger.info("title_day: %s", title_day)
        logger.info("Booking: %s", len(booking))

        if booking:
            bookings_in_string: list = tag_find_by_attr(booking, "title")

            # Se Encarga de extraer la informacion de la reserva
            # ponerla en un objeto Book y crear un objeto AirCraft
            stract_info_from_tag(bookings_in_string)

            serie,  file = clas_to_series(today, date)
            logger.info("Eliminar 0:  0;-0;; @")
            return serie, file, title_day
        else:
            logger.warning("No hay booking")

    # except Exception as e:
    #     print(f"Error en main(): {e}")

    finally:
        # Cerrar el navegador
        logger.info("Cerrando el navegador...")
        driver.close_driver()


if __name__ == '__main__':
    """
    Para ejecutar desde pc Local yq que tiene un arch AMD64
    """
    from src.app.utils.styles import main_styles
    hoy = False
    date = datetime.date.today if hoy else datetime.date.today() + \
        datetime.timedelta(days=1)
    main(hoy, hidden=False, architecture="amd64", date=date)
    main_styles(hoy, date=date)
