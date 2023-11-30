#!/bin/bash

echo 'DB_ENGINE=django.db.backends.postgresql' > .env
echo 'DB_NAME=postgres' >> .env
echo 'POSTGRES_USER=postgres' >> .env
echo 'POSTGRES_PASSWORD=postgres' >> .env
echo 'DB_HOST=127.0.0.1' >> .env
echo 'DB_PORT=5432' >> .env
echo 'DJANGO_SETTINGS_MODULE=yatube.settings' >> .env
