#!/bin/bash

python manage.py sqlclear | python manage.py dbshell;
python manage.py syncdb
