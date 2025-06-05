#!/usr/bin/env python
# coding: utf-8

# In[33]
import time
import datetime

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from src.app.utils.utils import clas_to_series
from src.app.utils.wdriver import CustomChromeDriver

from src.app.utils.page import (
    login_page,
    get_element_click_newPage,
    # close_popup_with_js,
    find_element
)
from src.app.utils.utils import save_Book_by_tag

# logging que esta el modulo (__init__.py)
from . import logger


def navigate_to_programming(
    today: bool = False,
    sleep: int = 2,
    driver: CustomChromeDriver = None,
    select_all: bool = False
):
    """
    Navigates to the programming page.

    Args:
        today (bool, optional): Flag indicating whether to navigate to today's programming. Defaults to False.
        sleep (int, optional): Number of seconds to sleep before continuing. Defaults to 2.
    """

    # eliminar wrapper, antes habia un popap
    # close_popup_with_js(driver, ".wrapper .ui-close")

    # navegar a programacion, icono program
    print("navegar a programacion")
    get_element_click_newPage(
        driver, xpath="/html/body/div[2]/div[1]/div/div[3]/ul/li[5]")

    show_filtro(driver, select_all=select_all)

    time.sleep(sleep)
    if not today:
        # Sigiente dia
        # <span class="datebtn ui-after"></span>
        get_element_click_newPage(driver, "span.ui-after")
        logger.info("siguiente dia")

    time.sleep(10)  # esperar que cargue la pagina


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


def navigate_in_filter(driver: CustomChromeDriver, time_sl: int = 4, select_all: bool = False):
    time.sleep(time_sl)

    def get_select_box_filter():
        # ver texto si tiene seleccionar todo o quitar todo
        text_select_all = find_element(
            driver, "/html/body/div[7]/div[3]/div/div[2]/div[5]/div[1]/div/label/span[2]").text

        logger.info("texto que hay en filtro:: %s", text_select_all)
        return text_select_all

    def get_html():
        # ver elementos
        el = find_element(
            driver, xpath="/html/body/div[7]/div[3]/div/div[2]/div[5]")
        html_str = el.get_attribute("outerHTML")
        logger.info(f"ele: {html_str}")

    text_select_all = get_select_box_filter()
    if text_select_all.lower() in ["seleccionar todo", "select all"]:
        # if select_all:
        # Seleccionar todos los filtros
        get_element_click_newPage(
            driver, xpath="/html/body/div[7]/div[3]/div/div[2]/div[5]/div[1]/div/label")

    else:  # quitar todo o Unselect all
        # 1r click deseleccionara todo
        get_element_click_newPage(
            driver, xpath="/html/body/div[7]/div[3]/div/div[2]/div[5]/div[1]/div/label")
        # seleccionara todo
        get_element_click_newPage(
            driver, xpath="/html/body/div[7]/div[3]/div/div[2]/div[5]/div[1]/div/label")

        # time.sleep(2)
        # desceleccionar Canceled

    time.sleep(1)
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

    get_html()
    time.sleep(1)
    # aceptar config
    get_element_click_newPage(
        driver, xpath="/html/body/div[7]/div[3]/div/div[3]/div[1]/button")
    time.sleep(5)  # permitir que se ajuste los cambios


def show_filtro(driver, time_sl: int = 4, select_all: bool = False):
    # ir a filtro
    time.sleep(time_sl-2)
    get_element_click_newPage(driver, "i.ui-filters")
    logger.info("click filtro")

    navigate_in_filter(driver, time_sl, select_all)


def tag_find_by_attr(list_tag: list, attr_tag: str):
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
        date: datetime.date = None,
        select_all: bool = False
):
    # from src.app.utils.wdriver import driver  # nopep8
    try:
        driver = CustomChromeDriver(
            hidden_windows=hidden,
        )
        login_page(driver)

        # # Configurar la hora local
        # config_hour_navigate(driver)

        # # desloagaer y volver a logear
        # logout(driver)
        # time.sleep(2)
        # login_page(driver)

        # toda la navegacion comienza aqui en esta funcion
        navigate_to_programming(today, driver=driver, select_all=select_all)

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

            *_, html_table = clas_to_series(today, date)
            logger.info("Eliminar 0:  0;-0;; @")
            return title_day, html_table
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
