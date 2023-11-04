#!/usr/bin/env python
# coding: utf-8

# In[33]:


import time

from bs4 import BeautifulSoup

from utils.utils import clas_to_series
from utils.wdriver import driver

from utils.page import login, get_element_click_newPage
from utils.utils import save_Book_by_tag

def main():
    login(driver)
    get_element_click_newPage(driver)
    time.sleep(2)

    # Sigiente dia
    # <span class="datebtn ui-after"></span>
    get_element_click_newPage(driver, "span.ui-after")
    print("siguiente dia")

    # CARGAMOS DATOS
    time.sleep(6)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    aircrafts = soup.select("div.ui-list")
    if aircrafts:
        print("lista===", len(aircrafts))
        
        for air in aircrafts:
            code_plane = air.select("div.col1 .subimg") #inof del plane
            res_plane = air.select("div.col2 .res") # donde se encuntran los vuelos
            print(code_plane)
            
            for res_individual in res_plane:
                for res in res_individual:
                    if "Mantenimiento" in res.attrs["title"]:
                        # print(code_plane.attrs)
                        continue

                    else:
                        title_plane: str = res.attrs["title"]
                        saved = save_Book_by_tag(title_plane)
                    

        clas_to_series()
        driver.quit()
        print("Eliminar 0:  0;-0;; @")
        
    else:
        print("No hay Aircraft")


if __name__ == '__main__':
    main()
