
from selenium import webdriver
from dotenv import load_dotenv
import os


load = load_dotenv('.env')
if load:
    print(".env Cargadas")

PAS = os.getenv("password")
USER = os.getenv("user")

# config webdriver
# Widows
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

# Linux
# BRAVE_PATH = "/usr/bin/brave-browser"
url = os.getenv("base_url")

# Configura las opciones de Brave
options = webdriver.ChromeOptions()
# no sandbox
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')

# Establece la ubicación del ejecutable de Brave
options.binary_location = BRAVE_PATH

# Inicializa un navegador Brave
driver = webdriver.Chrome(options=options)

# Ancho de 1024 píxeles y alto de 768 píxeles
driver.set_window_size(1024, 768)


# Abre una página web
driver.get(url)
