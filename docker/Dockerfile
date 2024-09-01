FROM python:3.9.19-slim-bullseye as builder

RUN apt-get update -y

COPY dependences /app/dependences

WORKDIR /app

RUN pip install --no-cache-dir dependences/Twisted-16.6.0-cp311-cp311-win_amd64.whl && \
    pip install --no-cache-dir -r /app/dependences/requirements.txt

# Segunda etapa
FROM python:3.9.19-slim-bullseye

WORKDIR /app

COPY .env .
COPY app/ .

# Copiamos los paquetes instalados de la primera etapa
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

CMD [ "/bin/sh" ]
