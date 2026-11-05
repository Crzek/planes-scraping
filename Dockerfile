FROM python:3.12-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends wkhtmltopdf curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
# Configurar la zona horaria
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# CA intermedia de private-radar: api4.private-radar.com no la envia en la
# cadena TLS. Se descarga de Sectigo, se verifica su huella SHA-256 (el build
# falla si no coincide) y se guarda en PEM fuera de /app.
# Si Sectigo reemite el intermedio, actualizar PR_CA_SHA256:
#   curl -fsSL "$PR_CA_URL" | sha256sum
ARG PR_CA_URL=http://crt.sectigo.com/SectigoPublicServerAuthenticationCADVR36.crt
ARG PR_CA_SHA256=8c54c334b66ba4e426772af4a3f9136c19a1aec729fdb28c535c07a5a4ef22e0
ENV API_EXTRA_CA_FILE=/usr/local/share/private-radar/sectigo-dv-r36.pem
RUN mkdir -p "$(dirname "$API_EXTRA_CA_FILE")" && \
    curl -fsSL "$PR_CA_URL" -o /tmp/pr-ca.der && \
    echo "$PR_CA_SHA256  /tmp/pr-ca.der" | sha256sum -c - && \
    python -c "import ssl,sys; open(sys.argv[2],'w').write(ssl.DER_cert_to_PEM_cert(open(sys.argv[1],'rb').read()))" \
        /tmp/pr-ca.der "$API_EXTRA_CA_FILE" && \
    rm /tmp/pr-ca.der

# Instalar uv
RUN pip install --no-cache-dir uv
    

WORKDIR /app

# Copiar lockfile y pyproject primero (cache de deps)
COPY pyproject.toml uv.lock ./

# Instalar dependencias con uv
RUN uv pip install --system -r pyproject.toml
# Instalar Chromium para Playwright (incluye deps del sistema)
RUN playwright install --with-deps chromium

COPY . /app

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]