#!/usr/bin/env bash

# use rsync to prep the app files for docker
#rsync -rv --relative -e "ssh -i /home/donagh/.ssh/server.pem" \
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
--exclude "scripts/" \
--exclude "build/" \
. deploy/app/

