from src.app.models.aircraft import AirCraft
from src.app.models.book import Book

import pandas as pd

from globals import START_DEL, END_DEL, TODAY, TOMORROW


# from src.app.test.export import excel_to_pdf

PLANES = []  # [DFG,GHG]
BOOKS = {}  # "DFR" :{"takeoff":[], "landing":[]}
No_Plane = {
    "EC-CVY",
    "EC-GV8",
    "D-0118",
    "EC-LYS	",
    "F-GBIM",
    "EC-KYA	",
    "EC-IXA",
    "EC-MZF	",
    "F-CFBX",
    "EC-FCD",
    "F-CESI",
    "EC-NMV",
    "F-CEGG",
    "D-KBIU",
    "EC-LGS",
    "ES-3A-096-7",
    "ES-3A-042",
}  # aviones excuidos


def save_Book_by_tag(cadena: str):
    """
    File: `src/app/utils/utils.py`
    Author: `g:crzek
    Email: `g:crzerick6@gmail.com
    Github: `g:crzek_github
    Description: 
    almacena la reserva en un objeto Book y crea un objeto AirCraft
    """
    hora, planeName, reservaName, *res = cadena.split("\n")

    if hora and planeName and reservaName:
        takeoff = hora[:5]  # 09:00
        landing = hora[6:]  # - 11:00
        # Cremos avion
        plane = AirCraft(planeName, "ok")
        # Reserva
        reserva = Book(takeoff, landing, reservaName, plane)
        # insertamos en reservas globales
        # AirCraft.add_reservas(reserva)
        plane.update_reservas(takeoff, landing)
        return True

    else:
        return False


def clas_to_series(today: bool = False):
    from globals import PATH_STATIC_DATA

    # Crear una serie de Pandas de ejemplo
    data = get_all_reservas(AirCraft.all_reservas)

    # 1r elemento del dic
    elem_dic_0 = list(data["books"].keys())[0]
    # indice de la serie
    # el siete tiene que coincidir con la funcion delete_0_salidas
    # def delete_0_salidas(array: list, delete_start: int = 6, delete_end: int = 4):
    serie = pd.DataFrame(data["books"], index=range(
        START_DEL, START_DEL+len(data["books"][elem_dic_0]))).transpose()

    # Exportar la serie a un archivo CSV
    file_excel = f"{PATH_STATIC_DATA}vuelos-{TODAY if today else TOMORROW}.xlsx"  # nopep8
    serie.to_excel(file_excel, startrow=2)
    print("Exito al cargar el Excel")

# convertir en HTML
# main(serie)
# excel_to_pdf(file_excel)

# hacer pruebas pytest


def get_all_reservas(all_book: dict):
    """
    File: `src/app/utils/utils.py`
    Author: `g:crzek
    Email: `g:crzerick@gmail.com
    Github: `g:crzek_github
    Description: 
    obtiene todas las reservas de los aviones
    """
    codigos = list(all_book.keys())
    PLANES = codigos
    for code in codigos:
        takeoffANDlanding: dict = all_book[code]
        takeoff: list = takeoffANDlanding["takeoff"]
        array_takeoff: list = replace_salidas(takeoff)
        BOOKS[code] = array_takeoff

    # return {
    #     "codes": PLANES,
    #     "books": BOOKS
    # }

    return delete_plane_by_Array(PLANES, BOOKS, No_Plane)

# hacer prubas pytest


def replace_salidas(takeoff: list):
    """genera un array de 24 horas, con sus respectivas salidas

    Args:
        takeoff (list): ["09:00", "11:00"]

    Returns:
        array: [0,0,0,0,0,0,0,0,0,9,0,11,0,0,0,0,0,0,0,0,0,0,0,0]
    """
    array24_horas = [None]*24
    if len(takeoff) != 0:
        for hour in takeoff:
            for index_zero in range(len(array24_horas)):
                # cogemos los 2 primeros digitos de la hora
                # 09:30 -> 09
                if int(hour[:2]) == index_zero:
                    array24_horas[index_zero] = hour

    return delete_0_salidas(array24_horas)


def delete_0_salidas(array: list, delete_start: int = START_DEL, delete_end: int = END_DEL):
    """Eliminar las salidas 0, pero solo las 7 primeras
        y las 5 ultimas

    Args:
        array (list): [0,0,0,0,0,0,0,0,0,9,0,11,0,0,0,0,0,0,0,0,0,0,0,0]

    Returns:
        list: [0,0,9,11,0,0,0,0,0]
    """
    return array[delete_start:-delete_end]


def delete_plane_by_Array(planes: list, books: dict, notPlane: list):
    """Delete books only not planes

    Args:
        planes ("list"): ["DFG","DRT"...]
        books (dict): {
            "DFG":{
                "takeoff":[],
                "landing":[],
            }
        }
        notPlane (list): ["DFG]
    """

    for code in notPlane:
        # eliminar del dict
        # del books[code]
        books.pop(code, f"No se encuentra {code}")
        # eliminar de la lista
        if code in planes:
            planes.remove(code)

    return {
        "codes": planes,
        "books": books,
    }
