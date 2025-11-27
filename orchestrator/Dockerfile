FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy



ENV DEBIAN_FRONTEND=noninteractive \

    PIP_DEFAULT_TIMEOUT=100



WORKDIR /app



# Copiem requirements și instalăm dependențele

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple



# Copiem tot proiectul

COPY . .



# Nu mai punem CMD fix

# Containerul va fi lansat manual cu "docker compose run"

ENTRYPOINT []

CMD []

