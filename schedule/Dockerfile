FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD password

ENV MYSQL_DATABASE=schedule_database

COPY ./database/01_create_database.sql /docker-entrypoint-initdb.d/data.sql

EXPOSE 3306