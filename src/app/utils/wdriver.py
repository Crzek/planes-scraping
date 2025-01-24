from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
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
        path_driver: str = PATH_DRIVER,
        hidden_windows=False,
        platform="linux",
        architecture="arm64",  # amd64
    ):
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = path_browser
        print("--- path_browser", path_browser)

        if hidden_windows:
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument('--headless')

        try:
            # chromium  ->_definir chromediiver, normalmente ("/usr/bin/chromedriver"
            if (path_driver is not None) or (path_driver != "") or (architecture == "arm64"):
                chrome_service = Service(path_driver)
                print("--- path_driver", path_driver)
                super().__init__(options=self.options, service=chrome_service)
            else:
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
    driver = CustomChromeDriver(
        sandbox=True, path_driver="/usr/bin/chromedriver")
    if driver:
        driver.navigate_to_url("http://google.com")
        driver.close_driver()
