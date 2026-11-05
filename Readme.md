# Vuelos

Muestra las salida de los vuelos del Aeropuerto de Sabadell

# Create files 
Crea el archivo `.env` basado en `.env.example`.

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
gunicorn -w 2 -b '0.0.0.0:5000' 'main:app'
```


# run
```shell
python main.py
```

## Fuente de datos: API primero, Playwright de respaldo

Los vuelos se pueden obtener directamente de la API de private-radar (login +
`getByFilterNew`) en lugar de navegar la web con Playwright.

- Se controla con `USE_API_FIRST` en `.env` (por defecto `false`: solo Playwright).
- Con `USE_API_FIRST=true` se intenta la API y, si falla (login rechazado,
  error de red o HTTP, timeout, respuesta con esquema inesperado o sin
  reservas utilizables), se ejecuta Playwright automaticamente.
- El log indica la fuente usada: `fuente de vuelos: api` o
  `fuente de vuelos: playwright` (y el motivo del fallback), sin credenciales.
- Otras variables opcionales: `API_LOGIN_URL`, `API_BOOKINGS_URL`,
  `API_TIMEOUT`, `API_EXTRA_CA_FILE` (ver `.env.example`).
- `api4.private-radar.com` no envia el certificado intermedio, por eso se
  versiona `certs/sectigo-dv-r36.pem` y se anade a las CAs de `certifi`. La
  verificacion TLS siempre esta activa.

```shell
# activar la API primero y generar vuelos desde la web
USE_API_FIRST=true uv run flask run --debug

# tests (no usan red ni credenciales)
uv run pytest
```

## Pendiente (cambio `api-first-scraper-with-playwright-fallback`)

Fuente de verdad: `openspec/changes/api-first-scraper-with-playwright-fallback/tasks.md`.

**OpenSpec (tareas sin cerrar)**
- [ ] 1.1 Rotar la contraseña de la cuenta de private-radar (se pegó en un chat).
- [ ] 1.3 Comparar el Excel de Playwright con el de la API del mismo día (confirmar reservas `PIC2`/`SPIC` y que la hora coincide).
- [ ] 4.2 Verificar que con `USE_API_FIRST=false` la página de vuelos sale igual que antes.
- [ ] 5.1 Con `USE_API_FIRST=true`, generar hoy y mañana y comparar con Playwright (log: `fuente de vuelos: api`).
- [ ] 5.2 Forzar fallo de la API (`API_LOGIN_URL` inválida) y comprobar el fallback (log: `fuente de vuelos: playwright`).
- [ ] 5.3 Revisar el log de una ejecución real: sin contraseña ni token.
- [ ] Activar `USE_API_FIRST=true` en producción tras comparar unos días, y archivar el cambio (`/opsx:archive`).

**Certificados (`certs/sectigo-dv-r36.pem`)**
- [ ] Comprobar que los Dockerfiles de `docker/` (`Dockerfile-py`, `-py-arm`, `-py-firefox`, `-playwright`) copian `certs/`; solo se verificó el `Dockerfile` raíz.
- [ ] Reconstruir la imagen (`docker compose up --build`) y probar el login por API dentro del contenedor; la prueba hecha usó una imagen antigua con `requests` instalado a mano.
- [ ] Añadir `requests` a `requirements.txt` si algún flujo lo sigue usando (hoy no lo incluye).
- [ ] Si private-radar corrige la cadena TLS de `api4`, el intermedio sobra; si cambian de emisor o caduca (2036), la API fallará y se usará Playwright.

## Notes
1.  Ver donde esta intalado chrome y chrome driver:
```shell
which google-chrome

google-chrome --version
chromedriver --version
```

### To install chromium and chromedriver for ARM64
[link to install chrome driver](https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/911)