# Vuelos

Muestra las salida de los vuelos del Aeropuerto de Sabadell

# Create files 
Crea este archivo primero
src/config/default.py
```python
SECRET_KEY = "key"
```

# Installation Local

[Notion refer](https://www.notion.so/erickcruz/WebScraping-97caab9b379846a58ad86389fa218ea7)

1. Primero instalar twister

```shell
# esenciales
pip install selenium
pip install beautifulsoup4
# manipular data
pip install pandas
pip install python-dotenv

#----- Requirements esenciales
pip install python-dotenv pandas selenium beautifulsoup4 openpyxl
#---

# otros
pip install requests # hacer solicitudes, suele estar instalda en PY
# en linux
pip install twister
# windows, mirar la carpeta dependences
pip install dependences/twister....
pip install lxml
pip install Scrapy  # para coger etiquetas de la web 

```

# Install Docker compose
```shelll
# produccion ARM arch
docker-compose -f docker/docker-compose-arm.pro.yml up --build

# produccion AMD arch
docker-compose -f docker/docker-compose.pro.yml up --build

# para desarrollo para debugar
docker-compose -f docker/docker-compose.dev.yml up --build

```
Dentro del contenedor, recuerda seleccionar el Interprete de python.


# Development
```shelll
# run container and attaching
docker compose -f docker/docker-compose.dev.yml run --rm vuelos-app bash

# into the continer run:

flask run --host 0.0.0.0 --debug --reload
```

## Local develoment
```shell
export ENV_FILE=chrome.env
flask run --debug --reload

```

# Production
```shelll
# servidor flask
flask run --host=0.0.0.0

# gunicorn
# -w -> workers
gunicorn -w 2 -b '0.0.0.0:5000' 'entrypoint:app'
```


# run
```shell
python main.py
```

## Notes
1.  Ver donde esta intalado chrome y chrome driver:
```shell
which google-chrome

google-chrome --version
chromedriver --version
```

### To install chromium and chromedriver for ARM64
[link to install chrome driver](https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/911)