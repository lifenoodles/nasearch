#!/usr/bin/env bash

python manage.py sqlclear shownotes | python manage.py dbshell;
python manage.py migrate
