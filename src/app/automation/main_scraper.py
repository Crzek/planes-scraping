from datetime import datetime
import logging

from playwright.async_api import Locator, Page, async_playwright, expect
from src.app.automation.secure import secure_click, secure_fill
from src.app.utils.utils import clas_to_series, save_Book_by_tag
from src.core.settings import Settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s')

settings = Settings()

logger = logging.getLogger(__name__)


async def login(page: Page):
    await secure_fill(page, '#email', settings.user)
    await secure_fill(page, '#component-outlined', settings.password.get_secret_value())
    await page.wait_for_timeout(2000)
    await secure_click(page, '#signInButton')
    await page.wait_for_load_state('networkidle')
    logger.info("Login completado")


async def calendario(page: Page):
    """
    Navega al calendario
    css selector: div#manubar lu li[itemid="calendar"]
    """
    try:
        logger.info("navegar a programacion")
        await secure_click(page, '#menubar > ul > li.ui-calendar > div.txt.uil-menu-calendar')
    except Exception as e:
        logger.error("Error al navegar al calendario: %s", e)
        await secure_click(page, '#leftmenu > div.menu-items > ul.ui-menu > li.ui-calendar > div.txt.uil-menu-calendar')
        # raise e
    await page.wait_for_load_state('domcontentloaded')


async def config_vista_calendario(page: Page, select_all: bool = False):
    """
    Configura la vista del calendario
    xpath selector: #calendar span[title="Filtros"] button
    """
    # abrir filtro
    await page.wait_for_timeout(2000)
    await secure_click(page, '#calendar span[title="Filtros"] button')
    logger.info("click filtro")

    await _navigate_in_filter(page, select_all=select_all)


async def _navigate_in_filter(page: Page, select_all: bool = False):
    await page.wait_for_timeout(4000)

    xpath_select_all = '/html/body/div[4]/div[3]/div/div[2]/div[5]/div[1]/div/label/span[2]'
    select_all_locator = page.locator(f'xpath={xpath_select_all}')

    # ver texto si tiene seleccionar todo o quitar todo
    try:
        text_select_all = await select_all_locator.text_content()
        logger.info("texto que hay en filtro:: %s", text_select_all)
    except Exception as e:
        logger.error("Error al obtener el texto del filtro: %s", e)
        text_select_all = "unselected all"

    if text_select_all and text_select_all.strip().lower() in ["seleccionar todo", "select all"]:
        await secure_click(page, f'xpath={xpath_select_all}')
    else:
        # 1r click deseleccionara todo
        await secure_click(page, f'xpath={xpath_select_all}')
        # 2o click seleccionara todo
        await secure_click(page, f'xpath={xpath_select_all}')

    await page.wait_for_timeout(1000)

    # desceleccionar Canceled
    await secure_click(page, 'xpath=/html/body/div[4]/div[3]/div/div[2]/div[5]/div[2]/div[15]/label/span[2]')
    # desceleccionar Maintenance
    await secure_click(page, 'xpath=/html/body/div[4]/div[3]/div/div[2]/div[5]/div[2]/div[16]/label/span[2]')
    # desceleccionar not avialable
    await secure_click(page, 'xpath=/html/body/div[4]/div[3]/div/div[2]/div[5]/div[2]/div[17]/label/span[2]')
    # desceleccionar type rating
    await secure_click(page, 'xpath=/html/body/div[4]/div[3]/div/div[2]/div[5]/div[2]/div[5]/label/span[2]')

    await page.wait_for_timeout(1000)
    # aceptar config
    await secure_click(page, 'xpath=/html/body/div[4]/div[3]/div/div[3]/div[1]/button')
    await page.wait_for_timeout(5000)
    logger.info("filtros configurados")


async def navigate_next_day(page: Page):
    """Navega al siguiente dia en el calendario"""
    await secure_click(page, 'span[title="Día siguiente"] button')
    logger.info("siguiente dia")


async def get_title_booking(page: Page) -> list[Locator]:
    """Obtiene el titulo del booking"""
    try:
        booking_list = await page.locator('.react-draggable').all()
        return booking_list
    except Exception as e:
        logger.error("Error al obtener reservas: %s", e)
        return None


async def delete_parts(page: Page):
    await page.evaluate("""
        () => {
            const h1 = Array.from(document.querySelectorAll('h1'))
                .find(el => el.textContent.trim().toLowerCase() === 'simuladores');
            if (h1) {
                // Eliminar todos los elementos posteriores
                let next = h1.nextElementSibling;
                while (next) {
                    const toRemove = next;
                    next = next.nextElementSibling;
                    toRemove.remove();
                }
                h1.remove();
            }
        }
    """)


async def navigation_planes(page: Page, today: bool = False, select_all: bool = False) -> list[Locator]:
    await login(page)
    logger.info("login completado")
    await calendario(page)
    # screem pagina programacion o calendario vuelos
    await page.screenshot(path="./calendario_abierto.png")
    logger.info("calendario abierto")
    await config_vista_calendario(page, select_all=select_all)
    logger.info("filtros configurados")

    # await page.wait_for_timeout(2000)
    if not today:
        logger.info("navegando al siguiente dia")
        await navigate_next_day(page)

    await page.wait_for_timeout(10000)
    logger.info('screem filtro y dia')
    await page.screenshot(path="./filtros_configurados.png")
    await delete_parts(page)
    bookings = await get_title_booking(page)
    # screen con filtro y dia
    return bookings


async def stract_info_from_tag(list_info: list[str]):
    """
    stract info de un string
    """
    for info in list_info:
        if "DUAL" in info or "PIC" in info:
            # incargado de guardar la reserva
            saved: bool = save_Book_by_tag(info)
            # print(info + "\n")


async def tag_find_by_attr(list_ele: list[Locator], attr_tag: str):
    """
    find tag by attribute and value

    input: list_tag, attr, value
    return : attributes values
    """
    try:
        list_vales = []
        for ele in list_ele:
            value = await ele.get_attribute(attr_tag)
            list_vales.append(value)
        return list_vales

    except KeyError as e:
        logger.error(
            f"KeyError: {e} - No se encontró el atributo '{attr_tag}' en uno de los tags, para buscar el Vuelo")
        return []


async def main_scraper(
    today: bool = False,
    hidden: bool = True,
    date: datetime.date = None,
    select_all: bool = False
):
    logger.info("iniciando scraper headless: %s", hidden)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=hidden)

        # para poder manejar las descargas
        async def handle_download(download):
            print(await download.path())
            print(f"Cloud download: {download.url}")
            await download.save_as("./downloads/")

        page: Page = await browser.new_page()
        page.set_default_timeout(14000)
        try:
            await page.goto(settings.base_url)
            bookings: list[Locator] = await navigation_planes(page, today=today, select_all=select_all)
            if bookings:
                bookings_str = await tag_find_by_attr(bookings, "title")
                logger.info("bookings_str found: %s", len(bookings_str))
                # Se Encarga de extraer la informacion de la reserva
                # ponerla en un objeto Book y crear un objeto AirCraft
                await stract_info_from_tag(bookings_str)
                logger.info("stract_info_from_tag completed")
                *_, html_table = clas_to_series(today=today, date=date)
                logger.info("clas_to_series completed")
                title_day = page.locator(
                    '#calendar > div > header > div > div.ScheduleToolbar_dateViewFormatAndTabs__ntr6c > div.SelectDate_datePicker__1EKcc > div.SelectDate_strDateLarge__30-sQ')
                logger.info("title_day located")
                return title_day, html_table
        except Exception as e:
            logger.error("Error en la navegación (no internet maybe): %s", e)
            return None, None
        finally:
            logger.info("Cerrando el navegador...")
            await browser.close()
