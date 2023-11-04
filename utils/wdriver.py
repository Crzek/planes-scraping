
from selenium import webdriver
from dotenv import load_dotenv
import os


load = load_dotenv('.env')
if load:
    print("VG Cargadas")

PAS = os.getenv("password")
USER = os.getenv("user")

# config webdriver
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
url = 'https://acbs.private-radar.com/'

# Configura las opciones de Brave
options = webdriver.ChromeOptions()
# Establece la ubicación del ejecutable de Brave
options.binary_location = BRAVE_PATH

# Inicializa un navegador Brave
driver = webdriver.Chrome(options=options)

# Abre una página web
driver.get(url)
