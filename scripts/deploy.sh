#!/usr/bin/env bash

set -eu

if [ "${#}" -ne 2 ]; then
    echo "Usage: ${0} <user@server> <identity_file>"
    exit 1
fi

server=${1}
identity_file=${2}

# use rsync to copy needed files
echo "Transferring files to ${server}"
rsync -a --relative -e "ssh -i ${identity_file}" \
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
. ${server}:~/venv/noagenda-db/noagenda-db/

command="source ~/venv/noagenda-db/bin/activate;"
command+="cd ~/venv/noagenda-db/noagenda-db;"
command+="python manage.py collectstatic --noinput;"
command+="./bin/reload-gunicorn.sh"
ssh -i ${identity_file} ${server} ${command}
echo "Deploy complete"
