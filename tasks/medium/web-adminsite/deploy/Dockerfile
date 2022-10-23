FROM php:7.4-apache

RUN apt update && apt install -y zip
COPY phpsrc.zip /tmp
RUN unzip /tmp/phpsrc.zip -d /var/www/
RUN rm -rf /var/www/html && mv /var/www/phpsrc/ /var/www/html
COPY users.json /users.json
