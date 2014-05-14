#!/bin/bash

python manage.py sqlclear shownotes | python manage.py dbshell;
python manage.py syncdb
