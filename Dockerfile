# This is a Work-in-Progress

FROM python:2.7
MAINTAINER Christopher Bull

# prerequisite packages.
RUN apt-get update && apt-get install -y -q \
python python-pip uwsgi-plugin-python

# Deployment folder
ENV APP_DIR /var/www/goshna
RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR

# Copy application and install requirements
COPY . $APP_DIR/
RUN pip install -r $APP_DIR/requirements.txt

# Connect to NGINX
COPY config/goshna-nginx.conf /etc/nginx/sites-enabled/
RUN nginx -s reload
