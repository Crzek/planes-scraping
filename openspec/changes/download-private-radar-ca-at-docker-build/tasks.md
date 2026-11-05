# Tasks

## 1. Imagen de producción x86_64 (raíz)

- [x] 1.1 Añadir al `Dockerfile` de la raíz el paso de `design.md` (decisión 3: `ARG PR_CA_URL`, `ARG PR_CA_SHA256`, `ENV API_EXTRA_CA_FILE=/usr/local/share/private-radar/sectigo-dv-r36.pem`, descarga con `curl -fsSL`, `sha256sum -c`, conversión DER→PEM con Python) antes de `COPY . /app`; verificar con `docker compose build` que el log muestra `/tmp/pr-ca.der: OK`
- [x] 1.2 Añadir `certs/` a `.dockerignore` y `.gitignore` y `git rm --cached certs/sectigo-dv-r36.pem`; verificar con `docker compose run --rm --entrypoint sh vuelos-app -c 'ls /app/certs; head -1 $API_EXTRA_CA_FILE'` que `/app/certs` no existe y el PEM empieza por `-----BEGIN CERTIFICATE-----`
- [x] 1.3 Añadir `API_EXTRA_CA_FILE=/usr/local/share/private-radar/sectigo-dv-r36.pem` a `environment` en `docker-compose.yml`; verificar con `docker compose config | grep API_EXTRA_CA_FILE` que sale la ruta absoluta aunque `.env` defina la relativa
- [x] 1.4 Comprobar que el build falla con huella errónea: `docker compose build --build-arg PR_CA_SHA256=$(printf '0%.0s' {1..64})` debe terminar con error de `sha256sum`
- [ ] 1.5 Con la imagen nueva y `USE_API_FIRST=true`, generar vuelos de un día desde la web y verificar en el log `fuente de vuelos: api` sin `tls_error`

## 2. Imágenes de desarrollo y Raspberry Pi (ARM64) — aplazado

Aplazado por decisión del usuario. Antes del paso del certificado: base `bullseye` → `bookworm` (apt da 404) y, en ARM, Python 3.11.9 → 3.12.

- [ ] 2.1 Añadir `curl` al `apt-get install` de `docker/Dockerfile-py` y el mismo paso de la tarea 1.1 en la etapa final; verificar con `docker compose -f docker/docker-compose.dev.yml build` (si falla por apt de `bullseye`, anotarlo en el README como pendiente y no cambiar la base en este cambio)
- [ ] 2.2 Añadir el mismo paso a la etapa final de `docker/Dockerfile-py-arm`; verificar que `docker build -f docker/Dockerfile-py-arm .` llega al paso y muestra `OK` (en x86 requiere `--platform linux/arm64` con QEMU/buildx; si no está disponible, revisar el diff y verificar en la Raspberry Pi)
- [ ] 2.3 Añadir `API_EXTRA_CA_FILE=/usr/local/share/private-radar/sectigo-dv-r36.pem` a `environment` en `docker/docker-compose.dev.yml` (crear la sección, hoy está comentada) y en `docker/docker-compose-arm.pro.yml`; verificar con `docker compose -f <fichero> config | grep API_EXTRA_CA_FILE`
- [ ] 2.4 Con el contenedor de desarrollo levantado (`run --rm vuelos-app bash`, repo montado en `/app`), verificar que `head -1 $API_EXTRA_CA_FILE` funciona

## 3. Documentación

- [x] 3.1 Actualizar `Readme.md`: sección Docker indicando que producción es Ubuntu x86_64 con `docker compose up --build` (raíz) y que ARM/Raspberry Pi es alternativa; explicar que el intermedio se descarga y verifica en el build, cómo actualizar `PR_CA_SHA256` y que `certs/` solo se usa en local; marcar o reescribir los pendientes de "Certificados"
- [x] 3.2 Actualizar `CLAUDE.md` (sección Docker: despliegue = raíz en Ubuntu x86_64; mención del certificado descargado) y la línea "Despliegue" de `openspec/config.yaml` (Ubuntu x86_64 con `docker-compose.yml`; Raspberry Pi vía `.github/workflows/raspi.yml` como alternativa)
- [x] 3.3 Actualizar el comentario de `API_EXTRA_CA_FILE` en `.env.example`: ruta relativa para local; en Docker la fija el compose
- [x] 3.4 Verificar con `openspec validate download-private-radar-ca-at-docker-build` que el cambio es válido

## Workflow follow-up

- Desplegar en el servidor Ubuntu (`git pull && docker compose up --build -d`) y comprobar `API_EXTRA_CA_FILE` dentro de `prod-planes-pw` (ver Migration Plan en `design.md`).
- Archivar el cambio con `/opsx:archive` tras verificarlo en producción.
