from app.models.aircraft import AirCraft
from app.models.book import Book

import pandas as pd

PLANES = []  # [DFG,GHG]
BOOKS = {}  # "DFR" :{"takeoff":[], "landing":[]}
No_Plane = [
    "EC-LYS",
    "EC-CZZ",
    "EC-FCD",
    "F-CESI",
    "ES-3A-096-7",
    "ES-3A-042"
]  # aviones excuidos


def save_Book_by_tag(cadena: str):
    hora, planeName, reservaName, *res = cadena.split("\n")

    if hora and planeName and reservaName:
        takeoff = hora[:5]
        landing = hora[6:]
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


def clas_to_series():
    import datetime

    # Crear una serie de Pandas de ejemplo
    data = get_all_reservas(AirCraft.all_reservas)

    # 1r elemento del dic
    elem_dic_0 = list(data["books"].keys())[0]
    # indice de la serie
    # el siete tiene que coincidir con la funcion delete_0_salidas
    # def delete_0_salidas(array: list, delete_start: int = 6, delete_end: int = 4):
    serie = pd.DataFrame(data["books"], index=range(
        6, 6+len(data["books"][elem_dic_0]))).transpose()
    # Exportar la serie a un archivo CSV
    serie.to_excel(
        f'app/data/vuelos-{datetime.date.today() + datetime.timedelta(days=1)}.xlsx')
    print("Exito al cargar el Excel")

# hacer pruebas pytest


def get_all_reservas(all_book: dict):
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


def delete_0_salidas(array: list, delete_start: int = 6, delete_end: int = 3):
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
