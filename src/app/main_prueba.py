import requests
from bs4 import BeautifulSoup


# import scrapy
url = "https://acbs.private-radar.com/"

# Para que la web no detecte que es un robot
encabezado = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebkit/537.36 (KHTML,like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

# contine todo la web
response = requests.get(url, headers=encabezado)

soup = BeautifulSoup(response.text)
