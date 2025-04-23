import pandas as pd
import pdfkit
from .. import logger


def generate_html_table(df: pd.DataFrame, date: str = None) -> str:
    """Genera una tabla HTML a partir de un DataFrame

    Args:
        df (pd.DataFrame): DataFrame a convertir

    Returns:
        str: Tabla HTML generada
    """
    # Convertir el DataFrame a HTML
    html_content = df.to_html()

    # Agregar estilos básicos al HTML
    styled_html = (
        f"<style>table {{border-collapse: collapse; width: 100%; text-align: center;}}"
        f"th, td {{border: 1px solid black; padding: 5px;}}</style>"
        f"<h3>{date}</h3>"
        f"{html_content}")
    return styled_html


def export_to_pdf(
        df: pd.DataFrame,
        output_path_html: str,
        output_path_pdf,
        date: str = None):
    """Exporta un DataFrame a un archivo PDF

    Args:
        df (pd.DataFrame): serie de datos o dataframe
        output_path (str): el archivo de salida donde se guardaran los datos
    """
    try:
        # Convertir el DataFrame a HTML
        html_content = df.to_html()

        # Guardamos el HTMLcontent str en un archivo.html
        with open(output_path_html, "w", encoding="utf-8") as f:
            content = (
                f"<style>table {{border-collapse: collapse; width: 100%; text-align: center;}}"
                f"th, td {{border: 1px solid black; padding: 5px;}}</style>"
                f"<h3>{date}</h3>"
                f"{html_content}")
            f.write(content)

        # Convertir el archivo HTML a PDF
        pdfkit.from_string(output_path_html, output_path_pdf)
        logger.info(f"✅ PDF generado: {output_path_pdf}")

    except Exception as e:
        logger.error("❌ ERROR al exportar a PDF:", e)


def save_file(html_content, output_path):
    # Guardar HTML en un archivo
    try:
        with open(output_path, "w") as f:
            f.write(html_content)
            print(f"{format} guardado en {output_path}")

    except Exception as e:
        logger.error("ERROR al guardar el {format}:", e)

        # # Cargar Excel
        # df = pd.read_excel("archivo.xlsx")

        # # Convertir DataFrame a HTML con estilos básicos
        # html_content = df.to_html(index=False)

        # # Guardar HTML en un archivo
        # html_path = "temp.html"
        # pdf_path = "salida.pdf"

        # with open(html_path, "w") as f:
        #     f.write(f"<style>table {{border-collapse: collapse; width: 100%;}} th, td {{border: 1px solid black; padding: 5px;}}</style>{html_content}")

        # # Convertir HTML a PDF
        # pdfkit.from_file(html_path, pdf_path)

        # print("✅ PDF generado con formato básico.")
