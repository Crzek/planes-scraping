#!/usr/bin/env python
# coding: utf-8

# In[33]
import time

from bs4 import BeautifulSoup

from src.app.utils.utils import clas_to_series
from src.app.utils.wdriver import driver

from src.app.utils.page import login, get_element_click_newPage, close_popup_with_js
from src.app.utils.utils import save_Book_by_tag


def navigate_to_programming(today: bool = False, sleep: int = 2):
    # eliminar wrapper
    close_popup_with_js(driver, ".wrapper .ui-close")
    # navegar a programacion
    print("navegar a programacion")
    get_element_click_newPage(driver)

    sacar_filtro(driver)

    time.sleep(sleep)
    if not today:
        # Sigiente dia
        # <span class="datebtn ui-after"></span>
        get_element_click_newPage(driver, "span.ui-after")
        print("siguiente dia")


def sacar_filtro(driver, time_sl: int = 4):
    # ir a filtro
    time.sleep(time_sl-2)
    get_element_click_newPage(driver, "i.ui-filters")
    print("click filtro")
    time.sleep(time_sl)
    # eliminar cancelado
    get_element_click_newPage(driver, "div.ui-cancel")

    time.sleep(time_sl+2)
    # aceptar config
    get_element_click_newPage(
        driver, None, '//*[@id="box-schedule-filters"]/div[1]/div[3]/button[1]')


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


def stract_info_from_tag(list_info: list):
    """
    stract info de un string
    """
    for info in list_info:
        if "DUAL" in info or "PIC" in info:
            saved = save_Book_by_tag(info)
            # print(info + "\n")


def main(today: bool = False):
    try:
        login(driver)
        navigate_to_programming(today)

        # Cargar los datos
        time.sleep(6)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # content = soup.select(".ScheduleLine_calendar__TUHwI")
        booking = soup.select(".BookingContainer_wrapper__VpZwN")

        if booking:
            bookings_in_string: list = tag_find_by_attr(booking, "title")
            stract_info_from_tag(bookings_in_string)
            clas_to_series(today)
            print("Eliminar 0:  0;-0;; @")
        else:
            print("No hay booking")

    finally:
        # Cerrar el navegador
        print("Cerrando el navegador...")
        driver.quit()


if __name__ == '__main__':
    from src.app.utils.styles import main_styles
    hoy = True
    main(hoy)
    main_styles(hoy)
