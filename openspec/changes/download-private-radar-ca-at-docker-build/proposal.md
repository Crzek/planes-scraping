# Proposal

## Why

Las consultas a la API de private-radar (`api4.private-radar.com`) necesitan el certificado intermedio `Sectigo Public Server Authentication CA DV R36`, porque el servidor no lo envía en la cadena TLS. Hoy ese certificado solo existe como fichero versionado en `certs/`, y los Dockerfiles no lo garantizan: el de desarrollo y el de la Raspberry Pi montan el código como volumen y nunca se comprobó que lo tengan. Queremos que la propia imagen Docker descargue y verifique el certificado al construirse, para que cualquier despliegue tenga la cadena completa sin depender de ficheros del repo.

Además, la documentación (README, `CLAUDE.md`, contexto de OpenSpec) presenta la Raspberry Pi/ARM como despliegue principal, cuando hoy el despliegue real es un servidor **Ubuntu x86_64** que usa `docker-compose.yml` + `Dockerfile` de la raíz.

## What Changes

- El `Dockerfile` de la raíz (despliegue en Ubuntu x86_64) descarga el intermedio de Sectigo desde su URL oficial (`http://crt.sectigo.com/SectigoPublicServerAuthenticationCADVR36.crt`) durante el build, lo convierte de DER a PEM, comprueba su huella SHA-256 y **falla el build** si no coincide o no se puede descargar.
- El certificado se guarda fuera de `/app` (ruta fija de sistema), para que los volúmenes `../:/app` de desarrollo y ARM no lo oculten, y la imagen fija `API_EXTRA_CA_FILE` a esa ruta absoluta.
- Se aplica el mismo paso al Dockerfile de desarrollo (`docker/Dockerfile-py`) y al de la Raspberry Pi (`docker/Dockerfile-py-arm`); sus compose (`docker/docker-compose.dev.yml`, `docker/docker-compose-arm.pro.yml`) fijan `API_EXTRA_CA_FILE` en `environment` para que un `.env` con ruta relativa no lo pise.
- `docker-compose.yml` de la raíz también fija `API_EXTRA_CA_FILE` en `environment`.
- `certs/` se añade a `.dockerignore` y a `.gitignore` y deja de versionarse (`git rm --cached`); la copia local sigue en disco para ejecutar sin Docker (`uv run flask run`) y el README explica cómo descargarla.
- Documentación: README, `CLAUDE.md` y `openspec/config.yaml` indican que el despliegue de producción es Ubuntu x86_64 con `docker-compose.yml` de la raíz; ARM/Raspberry Pi queda como alternativa. Se actualiza la sección "Pendiente → Certificados" del README.

Producción es el `Dockerfile` + `docker-compose.yml` de la raíz: es lo que se implementa primero. Los Dockerfiles de `docker/` (dev y ARM) quedan **aplazados** a otro momento: además del paso del certificado necesitan pasar de `bullseye` a `bookworm` (apt da 404) y, el ARM, de Python 3.11.9 a 3.12.

Fuera de alcance: cambiar el workflow `.github/workflows/raspi.yml` (sigue desplegando en la Raspberry Pi), los Dockerfiles `-py-firefox`, `-playwright` y `docker/Dockerfile` (no usados), y cualquier cambio en `src/app/api/client.py`, que ya acepta rutas absolutas.

## Capabilities

### New Capabilities
- `container-image`: cómo se construyen las imágenes Docker de la aplicación (despliegue x86_64, desarrollo y ARM) y qué garantizan en tiempo de ejecución; en este cambio, que incluyan la CA intermedia de private-radar descargada y verificada.

### Modified Capabilities
<!-- Ninguna: no hay specs principales en openspec/specs/. -->

## Impact

- Ficheros: `Dockerfile`, `docker-compose.yml`, `docker/Dockerfile-py`, `docker/docker-compose.dev.yml`, `docker/Dockerfile-py-arm`, `docker/docker-compose-arm.pro.yml`, `.dockerignore`, `.gitignore`, `.env.example`, `Readme.md`, `CLAUDE.md`, `openspec/config.yaml`.
- El build necesita salida HTTP a `crt.sectigo.com`; sin red el build falla (intencionado).
- Si Sectigo reemite o cambia el intermedio, hay que actualizar la huella en los Dockerfiles; si private-radar corrige su cadena TLS, el paso sobra pero no estorba.
- Sin cambios en código Python, base de datos ni dependencias.
