#!/usr/bin/env bash

# use rsync to copy needed files
rsync -rv --relative -e "ssh -i /home/donagh/.ssh/server.pem" \
--exclude "*.pyc" \
--exclude "whoosh_index" \
--exclude "cleaned_settings.py" \
--exclude "settings_dev.py" \
--exclude ".git" \
--exclude ".gitignore" \
--exclude "*.opml" \
--exclude "*.fuse*" \
--exclude "*.sublime-*" \
--exclude "scripts/" \
--exclude "deploy/" \
--exclude "todo.txt" \
. ubuntu@54.213.153.244:~/venv/noagenda-db/noagenda-db/

ssh -i ~/.ssh/server.pem ubuntu@54.213.153.244 "source ~/venv/noagenda-db/bin/activate;cd ~/venv/noagenda-db/noagenda-db;python manage.py collectstatic --noinput"
