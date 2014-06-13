FROM ubuntu
MAINTAINER Donagh Hatton

# hack to get around lack of daemons in docker
RUN dpkg-divert --local --rename --add /sbin/initctl

RUN apt-get update
RUN apt-get -y install mysql-server

RUN sed -i -e "s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf
RUN sed -i -e "s/^port\s*=\s*3306/port = 3310/" /etc/mysql/my.cnf
# ADD setup-mysql.sh /opt/setup.sh

EXPOSE 3310

CMD mysqld_safe
