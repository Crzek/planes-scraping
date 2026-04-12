import logging
from playwright.async_api import Locator, Page

logger = logging.getLogger(__name__)

async def secure_click(page: Page, selector: str):
    try:
        await page.wait_for_selector(selector, timeout=20000)
        await page.click(selector)
    except Exception as e:
        logger.error(f"Error al hacer click en {selector}: {e}")
        return False
    return True

async def secure_fill(
    page: Page,
    selector: str,
    value: str,
    locator_parent: Locator = None,
    formato: bool = False,
):
    try:
        if locator_parent:
            locator = locator_parent.locator(selector)
            await locator.fill(value)
        else:
            await page.wait_for_selector(selector, timeout=20000)
            await page.fill(selector, value)
    except Exception as e:
        logger.error(f"Error al llenar {selector} con {value}: {e}")
        return False
    return True