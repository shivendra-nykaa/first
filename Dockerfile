FROM ubuntu:18.04
RUN apt-get clean 
RUN apt-get update && apt-get install -y software-properties-common
RUN DEBIAN_FRONTEND="noninteractive" TZ="Asia/Kolkata" apt-get -y install tzdata
RUN apt install -y nginx
RUN apt-get update --fix-missing
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update -y
RUN apt-get install -y libpq-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev libffi-dev libcurl4-openssl-dev libapache2-mod-wsgi-py3 curl
RUN apt-get install -y build-essential python3.8 python3.8-dev python3-pip python3.8-venv && apt-get install -y git
RUN apt install libmysqlclient-dev libcurl4-openssl-dev libssl-dev  -y
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor
RUN pip3 install --upgrade pip
RUN pip3 install uwsgi
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
RUN useradd --no-create-home nginx
RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache
RUN mkdir -p /var/log/uwsgi/
COPY server-conf/nginx.conf /etc/nginx/
COPY server-conf/flask-app-nginx.conf /etc/nginx/conf.d/
COPY /app/uwsgi.ini /etc/uwsgi/
COPY server-conf/supervisord.conf /etc/supervisor/
COPY app /app/src
WORKDIR /src
CMD ["/usr/bin/supervisord"]
