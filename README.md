# Zadanie rekrutacyjne

## Wymagania

Do uruchomienia projektu potrzebne są:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Konfiguracja

1. Stwórz plik .env na podstawie env_sample:
2. Zbuduj obrazy:
   ```bash
   docker compose -f docker-compose-dev.yml build
3. Zaimplementuj migracje
   ```bash
   docker compose -f docker-compose-dev.yml run --rm web python manage.py migrate

4. Uruchom kontenery:
   ```bash
   docker compose -f docker-compose-dev.yml up
5. Aplikacja uruchomi się w trybie developerskim na 127.0.0.1:{wybrany port DJANGO_EXTERNAL_PORT}
6. Domyślnym adresem jest http://127.0.0.1:8000/