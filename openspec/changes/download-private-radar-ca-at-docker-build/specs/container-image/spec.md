# Spec Delta

## Purpose

Define qué garantiza la imagen Docker de la aplicación (`Dockerfile` + `docker-compose.yml` de la raíz, en producción Ubuntu x86_64 y en el PC) al construirse y al arrancar, en particular la confianza TLS necesaria para la API de private-radar.

## ADDED Requirements

### Requirement: La imagen descarga la CA intermedia de private-radar al construirse
La imagen de la aplicación (`Dockerfile` de la raíz, usada en producción Ubuntu x86_64 y en desarrollo en el PC) SHALL descargar durante el build el certificado `Sectigo Public Server Authentication CA DV R36` desde la URL oficial de Sectigo y guardarlo en formato PEM dentro de la imagen, sin depender de la copia versionada en `certs/`.

#### Scenario: Build con red disponible
- **WHEN** se ejecuta `docker compose up --build` con `docker-compose.yml` de la raíz en un host Ubuntu x86_64 con acceso a `crt.sectigo.com`
- **THEN** el build termina correctamente y la imagen contiene el certificado intermedio en PEM en una ruta fija fuera de `/app`

### Requirement: El build falla si el certificado no es el esperado
El build SHALL verificar la huella SHA-256 del certificado descargado contra el valor fijado (`8C:54:C3:34:B6:6B:A4:E4:26:77:2A:F4:A3:F9:13:6C:19:A1:AE:C7:29:FD:B2:8C:53:5C:07:A5:A4:EF:22:E0`) y MUST abortar si la descarga falla o la huella no coincide.

#### Scenario: Descarga fallida
- **WHEN** `crt.sectigo.com` no responde o devuelve un error HTTP durante el build
- **THEN** el build termina con error y no se genera la imagen

#### Scenario: Huella distinta
- **WHEN** el fichero descargado tiene una huella SHA-256 distinta de la fijada
- **THEN** el build termina con error indicando que la huella no coincide

### Requirement: El contenedor usa el certificado descargado para la API
El contenedor levantado con `docker-compose.yml` SHALL tener `API_EXTRA_CA_FILE` apuntando a la ruta absoluta del certificado descargado, aunque el `.env` defina otra ruta.

#### Scenario: .env con ruta relativa
- **WHEN** el `.env` define `API_EXTRA_CA_FILE=certs/sectigo-dv-r36.pem` y se levanta `docker-compose.yml`
- **THEN** dentro del contenedor `API_EXTRA_CA_FILE` vale `/usr/local/share/private-radar/sectigo-dv-r36.pem`

#### Scenario: Login por API dentro del contenedor
- **WHEN** con `USE_API_FIRST=true` la aplicación hace login contra `api4.private-radar.com` desde el contenedor
- **THEN** la verificación TLS se completa sin `tls_error` y con la verificación de certificados activa

### Requirement: El certificado no se versiona ni entra en el build
El repositorio MUST NOT versionar `certs/` y el contexto de build MUST excluirlo, para que ninguna imagen dependa de una copia local. Para ejecutar fuera de Docker, la documentación SHALL indicar cómo descargar el certificado a `certs/sectigo-dv-r36.pem`.

#### Scenario: Ejecución local sin Docker
- **WHEN** se ejecuta `uv run flask run` en el host sin definir `API_EXTRA_CA_FILE`
- **THEN** la aplicación usa `certs/sectigo-dv-r36.pem` descargado en el host

#### Scenario: Ficheros ignorados
- **WHEN** se ejecuta `git status` tras descargar el certificado en `certs/`
- **THEN** `certs/` no aparece como cambio y la imagen de producción no contiene `/app/certs`
