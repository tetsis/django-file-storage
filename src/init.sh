#!/bin/sh

python manage.py makemigrations model
python manage.py migrate