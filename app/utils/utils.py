from app.models.aircraft import AirCraft
from app.models.book import Book

import pandas as pd

PLANES = []  # [DFG,GHG]
BOOKS = {}  # "DFR" :{"takeoff":[], "landing":[]}
No_Plane = ["EC-LYS", "EC-CZZ", "EC-FCD",
            "F-CESI", "ES-3A-096-7"]  # aviones excuidos


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
    serie = pd.DataFrame(data["books"])
    # print(serie)
    # option = str(input("Quieres convertir a excel: (Y/n)")).upper()
    # if option == "Y":
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
    # 0,0,0,0,0,0,0,0,0,0
    # 9,13
    # arra0 = [0] * (20-7 + 1)
    arra0 = [0]*24
    if len(takeoff) != 0:
        for hour in takeoff:
            for index_zero in range(len(arra0)):  # aqui esta el error
                if int(hour[:2]) == index_zero:
                    # modificar aqui si se quieren los minutos
                    arra0[index_zero] = hour
        return arra0


def generate_hour(takeoff: list):
    # itermos takeoff para genera un horario en un aarray
    # 0,0,0,0,0,0,0,0,0,9,0,11
    if len(takeoff) > 0:
        for index in range(20):  # 9,13
            pass


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
