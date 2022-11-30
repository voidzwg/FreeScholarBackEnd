#!/bin/bash
python /var/www/html/backend/manage.py makemigrations
python /var/www/html/backend/manage.py migrate
uwsgi --ini /var/www/html/backend/uwsgi.ini
python /var/www/html/backend/manage.py runserver 8001