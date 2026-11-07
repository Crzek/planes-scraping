# Design

## Context

- `src/app/api/client.py::build_ca_bundle` ya junta las CAs de `certifi` con el fichero de `API_EXTRA_CA_FILE` (texto PEM) y acepta rutas absolutas; el valor por defecto (`src/core/settings.py`) es la ruta relativa `certs/sectigo-dv-r36.pem`. No hace falta tocar Python.
- Despliegue real: Ubuntu x86_64 con `docker-compose.yml` + `Dockerfile` de la raíz (`python:3.12-slim-bookworm`, `COPY . /app`, sin volumen). Desarrollo (`docker/Dockerfile-py`) y ARM (`docker/Dockerfile-py-arm`) montan el repo con `../:/app`, lo que tapa cualquier fichero que la imagen haya dejado en `/app`.
- Sectigo publica el intermedio en DER en `http://crt.sectigo.com/SectigoPublicServerAuthenticationCADVR36.crt` (es la URL `CA Issuers` del certificado de `*.private-radar.com`). Comprobado: la descarga actual tiene la misma huella SHA-256 que `certs/sectigo-dv-r36.pem` (`8C54C334…A4EF22E0`).
- El `.env` actual no define `API_EXTRA_CA_FILE`; `.env.example` sí, con la ruta relativa.

## Goals / Non-Goals

**Goals:**
- Un único paso de build, idéntico en los tres Dockerfiles, que descarga, verifica y deja el PEM en una ruta fija.
- Que el contenedor use esa ruta aunque haya volumen en `/app` o un `.env` con la ruta relativa.

**Non-Goals:**
- Instalar la CA en el almacén del sistema (`update-ca-certificates`): `requests` usa `certifi`, no el almacén del sistema.
- Descargar el certificado en tiempo de arranque (`entrypoint.sh`).
- En esta iteración, los Dockerfiles de `docker/` (dev y ARM): aplazados por decisión del usuario; producción es el `Dockerfile` raíz.

## Decisions

1. **Ruta fija fuera de `/app`: `/usr/local/share/private-radar/sectigo-dv-r36.pem`.** Sobrevive a los volúmenes `../:/app`. Alternativa descartada: `/app/certs/`, que el volumen de dev/ARM oculta.

2. **Verificar con huella SHA-256 fijada como `ARG`.** `ARG PR_CA_URL` y `ARG PR_CA_SHA256` (hex sin dos puntos) en cada Dockerfile; se comprueba el DER descargado con `echo "$PR_CA_SHA256  ca.der" | sha256sum -c -`. La huella SHA-256 de un certificado es el hash de su DER, así que coincide con la de `openssl x509 -fingerprint`. La descarga es por HTTP (así la publica Sectigo); la huella es lo que da integridad. Alternativa descartada: confiar en la descarga sin verificar.

3. **Conversión DER→PEM con Python (`ssl.DER_cert_to_PEM_cert`).** Python está en todas las imágenes; evita depender de que el CLI `openssl` esté instalado en las `slim`. Descarga con `curl -fsSL` (el `Dockerfile` raíz ya instala `curl`; en `Dockerfile-py` se añade `curl` al `apt-get install` existente; `Dockerfile-py-arm` parte de la imagen completa, que lo trae).

   Paso de referencia (igual en los tres):
   ```dockerfile
   ARG PR_CA_URL=http://crt.sectigo.com/SectigoPublicServerAuthenticationCADVR36.crt
   ARG PR_CA_SHA256=8c54c334b66ba4e426772af4a3f9136c19a1aec729fdb28c535c07a5a4ef22e0
   ENV API_EXTRA_CA_FILE=/usr/local/share/private-radar/sectigo-dv-r36.pem
   RUN mkdir -p /usr/local/share/private-radar && \
       curl -fsSL "$PR_CA_URL" -o /tmp/pr-ca.der && \
       echo "$PR_CA_SHA256  /tmp/pr-ca.der" | sha256sum -c - && \
       python -c "import ssl,sys;open(sys.argv[2],'w').write(ssl.DER_cert_to_PEM_cert(open(sys.argv[1],'rb').read()))" \
           /tmp/pr-ca.der "$API_EXTRA_CA_FILE" && \
       rm /tmp/pr-ca.der
   ```
   Se coloca antes de `COPY . /app` para que quede cacheado entre builds.

4. **`API_EXTRA_CA_FILE` en `ENV` de la imagen y en `environment` de cada compose.** En compose, `environment` tiene prioridad sobre `env_file`, así un `.env` copiado de `.env.example` no lo pisa. Alternativa descartada: solo `ENV` en la imagen (lo pisa `env_file`).

5. **`certs/` en `.dockerignore` y `.gitignore`, sin versionar.** La copia local (descargada con el comando del README) sirve para `uv run flask run` en el host. Excluirla del contexto garantiza que la imagen raíz no la use por accidente. En dev/ARM sigue visible por el volumen, pero no se usa porque `API_EXTRA_CA_FILE` es absoluto.

## Risks / Trade-offs

- [Build sin acceso a `crt.sectigo.com`] → falla el build a propósito; el mensaje de `curl`/`sha256sum` indica la causa. Se puede reintentar o, en caso extremo, pasar otra URL con `--build-arg PR_CA_URL=…`.
- [Sectigo reemite el intermedio o private-radar cambia de emisor] → la huella no coincide y el build falla; hay que actualizar `PR_CA_SHA256` (y la copia de `certs/`). Documentarlo en el README.
- [`docker/Dockerfile-py` y `-py-arm` usan base `bullseye`: comprobado que `apt-get install` da 404 en `debian-security`] → al retomarlos, pasar a `bookworm` (probado: ambos construyen; el ARM solo en amd64 sin `--platform`) y el ARM a Python 3.12 (`requires-python = "==3.12.*"`).
- [Un clon nuevo no trae `certs/`] → con `USE_API_FIRST=true` en local la API falla (`ca_file_missing`) y se usa Playwright hasta descargar el certificado con el comando del README.
- [Huella duplicada en tres Dockerfiles] → aceptado frente a crear un script compartido; son tres líneas `ARG` fáciles de buscar.

## Migration Plan

1. En el servidor Ubuntu: `git pull` y `docker compose up --build -d` (usa `docker-compose.yml` de la raíz).
2. Comprobar `docker exec prod-planes-pw sh -c 'echo $API_EXTRA_CA_FILE && head -1 $API_EXTRA_CA_FILE'`.
3. Rollback: volver al commit anterior y reconstruir; la imagen anterior usaba `certs/` copiado por `COPY . /app`.
