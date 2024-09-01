#!/usr/bin/env python
# coding: utf-8

# In[33]
import time

from bs4 import BeautifulSoup

from app.utils.utils import clas_to_series
from app.utils.wdriver import driver

from app.utils.page import login, get_element_click_newPage, close_popup_with_js
from app.utils.utils import save_Book_by_tag


def navigate_to_programming(sleep: int = 2):
    # eliminar wrapper
    close_popup_with_js(driver, ".wrapper .ui-close")
    # navegar a programacion
    print("navegar a programacion")
    get_element_click_newPage(driver)

    time.sleep(sleep)
    # Sigiente dia
    # <span class="datebtn ui-after"></span>
    get_element_click_newPage(driver, "span.ui-after")
    print("siguiente dia")


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


def main():
    try:
        login(driver)
        navigate_to_programming()

        # Cargar los datos
        time.sleep(6)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.select(".ScheduleLine_calendar__TUHwI")
        booking = soup.select(".BookingContainer_wrapper__VpZwN")

        if booking:
            bookings_in_string: list = tag_find_by_attr(booking, "title")
            stract_info_from_tag(bookings_in_string)
            clas_to_series()
            print("Eliminar 0:  0;-0;; @")
        else:
            print("No hay Aircraft")

    finally:
        # Cerrar el navegador
        print("Cerrando el navegador...")
        driver.quit()


if __name__ == '__main__':
    main()
