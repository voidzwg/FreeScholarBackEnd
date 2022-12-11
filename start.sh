#!/bin/bash
project=backend
base=/var/www/html
# project=FreeScholarBackEnd
# base=/root/FreeScholar
python $base/$project/manage.py makemigrations
python $base/$project/manage.py migrate
uwsgi --ini $base/$project/uwsgi.ini
python $base/$project/manage.py runserver 0.0.0.0:8000