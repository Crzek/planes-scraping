#!/usr/bin/env python
# coding: utf-8

# In[33]
import time

from bs4 import BeautifulSoup

from src.app.utils.utils import clas_to_series
from src.app.utils.wdriver import CustomChromeDriver

from src.app.utils.page import login_page, get_element_click_newPage, close_popup_with_js
from src.app.utils.utils import save_Book_by_tag


def navigate_to_programming(today: bool = False, sleep: int = 2, driver: CustomChromeDriver = None):
    """
    Navigates to the programming page.

    Args:
        today (bool, optional): Flag indicating whether to navigate to today's programming. Defaults to False.
        sleep (int, optional): Number of seconds to sleep before continuing. Defaults to 2.
    """

    # eliminar wrapper
    close_popup_with_js(driver, ".wrapper .ui-close")

    # navegar a programacion
    print("navegar a programacion")
    get_element_click_newPage(driver)

    show_filtro(driver)

    time.sleep(sleep)
    if not today:
        # Sigiente dia
        # <span class="datebtn ui-after"></span>
        get_element_click_newPage(driver, "span.ui-after")
        print("siguiente dia")


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
    print("click filtro")

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


def main(today: bool = False, hidden: bool = False):
    # from src.app.utils.wdriver import driver  # nopep8
    try:
        driver = CustomChromeDriver(hidden_windows=hidden)
        login_page(driver)
        # toda la navegacion comienza aqui en esta funcion
        navigate_to_programming(today, driver=driver)

        # Cargar los datos
        time.sleep(6)
        print("Cargando los datos...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Eliminar partes innecesarias
        delete_parts(soup)

        booking = soup.select(".BookingContainer_wrapper__VpZwN")

        if booking:
            bookings_in_string: list = tag_find_by_attr(booking, "title")

            # Se Encarga de extraer la informacion de la reserva
            # ponerla en un objeto Book y crear un objeto AirCraft
            stract_info_from_tag(bookings_in_string)

            clas_to_series(today)
            print("Eliminar 0:  0;-0;; @")
        else:
            print("No hay booking")

    # except Exception as e:
    #     print(f"Error en main(): {e}")

    finally:
        # Cerrar el navegador
        print("Cerrando el navegador...")
        driver.close_driver()


if __name__ == '__main__':
    from src.app.utils.styles import main_styles
    hoy = False
    main(hoy)
    main_styles(hoy)
