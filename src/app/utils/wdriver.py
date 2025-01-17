from selenium import webdriver
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.chrome.service import Service
from globals import PATH_BROWSER, URL, PATH_DRIVER

"""
    Mirar archivo test/webdriver.py
    Es donde se encutra el código original que funciona en contenedor
"""


class CustomChromeDriver(webdriver.Chrome):
    def __init__(
        self,
        path_browser: str = PATH_BROWSER,
        url: str = URL,
        driver_path: str = PATH_DRIVER,
        hidden_windows=False
    ):
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = path_browser

        if hidden_windows:
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument('--headless')

        # Crear el servicio de Chrome
        # chrome_service = Service(driver_path)

        try:
            # super().__init__(service=chrome_service, options=self.options)
            super().__init__(options=self.options)
            self.set_window_size(1024, 768)
        except WebDriverException as e:
            print(f"Error al inicializar el navegador: {e}")

        self.navigate_to_url(url)

    def navigate_to_url(self, url):
        try:
            self.get(url)
        except WebDriverException as e:
            print(f"Error al navegar a la URL {url}: {e}")

    def close_driver(self):
        try:
            self.close()
            self.quit()
        except WebDriverException as e:
            print(f"Error al cerrar el navegador: {e}")


# Ejemplo de uso
if __name__ == "__main__":
    driver = CustomChromeDriver(sandbox=True)
    if driver:
        driver.navigate_to_url("http://google.com")
        driver.close_driver()
