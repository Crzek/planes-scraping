from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


options = Options()
options.add_argument("--headless")  # Opcional: sin interfaz gráfica
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# Directorio temporal único
# options.add_argument("--user-data-dir=/tmp/selenium_user_data")

# Reemplaza con la ruta correcta a tu ChromeDriver
# s = Service(executable_path="/usr/bin/chromedriver")
s = Service(executable_path="/usr/bin/chromium")
driver = webdriver.Chrome(options=options, service=s)


driver.get("https://google.com/")
print(driver.title)
driver.quit()
