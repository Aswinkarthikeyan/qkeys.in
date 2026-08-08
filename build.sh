#!/usr/bin/env bash

apt-get update

apt-get install -y \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libfontconfig1 \
    libfreetype6 \
    libjpeg62-turbo \
    libopenjp2-7 \
    libffi8

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate