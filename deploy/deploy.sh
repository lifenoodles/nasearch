#!/usr/bin/env bash

rsync -rv --relative -e "ssh -i /home/donagh/.ssh/server.pem" \
--exclude "*.pyc" \
--exclude "whoosh_index" \
--exclude "cleaned_settings.py" \
--exclude "settings_dev.py" \
--exclude ".git" \
--exclude ".gitignore" \
--exclude "deploy.sh" \
--exclude "*.opml" \
--exclude "*.fuse*" \
--exclude "*.sublime-*" \
. "$1":~/venv/noagenda-db/noagenda-db/

