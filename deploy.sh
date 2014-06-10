#!/usr/bin/env bash

rsync -rv --relative \
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
. "$1":~/www/noagendadb/

