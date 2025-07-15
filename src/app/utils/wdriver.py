import logging
import platform
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from globals import PATH_BROWSER, URL, PATH_DRIVER, ENV_FILE

# Configuración básica del logger
logger = logging.getLogger(__name__)
"""
    Mirar archivo test/webdriver.py
    Es donde se encutra el código original que funciona en contenedor
"""


class CustomChromeDriver(webdriver.Chrome):
    def __init__(
        self,
        path_browser: str = PATH_BROWSER,
        url: str = URL,
        path_driver: str = PATH_DRIVER,
        hidden_windows=False,
        # platform="linux",
        # architecture="x86_64",  # 'x86_64', 'arm64'
    ):
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = path_browser
        
        architecture_os = platform.machine()  # 'x86_64', 'arm64':
        
        # logs info
        logger.info("--- path_browser %s", path_browser)
        logger.info("--- path_driver %s", path_driver)
        logger.info("debug hidden-windows: %s", hidden_windows)
        logger.info("debug platform: %s", platform.machine())

        # si se oculta el navegador o es arm64
        if hidden_windows or architecture_os == "arm64":
            logger.info("Modo Sin Ventana Activado")
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument('--headless')

        try:
            # system = platform.system()  # 'Linux', 'Windows'
            logger.info("system Machine: %s", architecture_os)
            # chromium  ->_definir chromediiver, normalmente ("/usr/bin/chromedriver"
            if architecture_os == "aarch64":  # arm64
                logger.info(
                    "Architecture: ARM64, ha ingresado en el bloque chromium")
                # if (path_driver is not None) or (path_driver != "") or (architecture == "arm64"):
                chrome_service = Service(path_driver)
                logger.info(
                    "--- path_driver, %s env: %s", path_driver, ENV_FILE)
                super().__init__(options=self.options, service=chrome_service)
            else:
                super().__init__(options=self.options)

            self.set_window_size(1024, 768)

        except WebDriverException as e:
            logger.critical(f"Error al inicializar el navegador: {e}")

        self.navigate_to_url(url)

    def navigate_to_url(self, url):
        try:
            self.get(url)
        except WebDriverException as e:
            logger.error(f"Error al navegar a la URL {url}: {e}")

    def close_driver(self):
        try:
            self.close()
            self.quit()
        except WebDriverException as e:
            logger.error(f"Error al cerrar el navegador: {e}")


# Ejemplo de uso
print("__name__", __name__)
if __name__ == "__main__":
    driver = CustomChromeDriver(
        sandbox=True, path_driver="/usr/bin/chromedriver")
    if driver:
        driver.navigate_to_url("http://google.com")
        driver.close_driver()
