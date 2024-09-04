import asposecells
from asposecells.api import Workbook, FileFormatType, PdfSaveOptions
import pandas as pd

excel = "app/data/_vuelos-2024-09-03.xlsx"

"""EXport excel to PDF
        cREO QUE ES meJOR USAR OTRO LENGUAJE PARA ESTO
    """


def main(frame: pd.DataFrame):
    # frame.read_excel(excel)
    # print("Exito al cargar el Excel")

    frame.to_html("app/data/vuelos.html")
    print("Exito al cargar el HTML")


if __name__ == '__main__':
    main()
