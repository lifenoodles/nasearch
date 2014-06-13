FROM ubuntu
MAINTAINER Donagh Hatton

# hack to get around lack of daemons in docker
RUN dpkg-divert --local --rename --add /sbin/initctl

RUN apt-get update
RUN apt-get -y install nginx python-pip libmysqlclient-dev libxslt1-dev python-dev supervisor
RUN pip install gunicorn django requests opml feedparser django-haystack whoosh BeautifulSoup4 MySQL-python
RUN mkdir -p /var/log/supervisor

ADD deploy/app /opt/noagenda-db/
ADD deploy/nginx-config /etc/nginx/sites-available/no-agendadb
RUN ln -s /etc/nginx/sites-available/no-agendadb /etc/nginx/sites-enabled/no-agendadb
RUN rm /etc/nginx/sites-enabled/default
RUN sed -i '1s/^/daemon off;\n/' /etc/nginx/nginx.conf

VOLUME /opt/noagenda-db/nadb

# ADD supervisor config
ADD deploy/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

WORKDIR /opt/noagenda-db

# collect static files for django deploy
RUN python manage.py collectstatic --noinput
RUN python manage.py syncdb

EXPOSE 80

CMD supervisord
