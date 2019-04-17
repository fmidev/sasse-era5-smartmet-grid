# PostgreSQL container for Fminames database without replication from FMI master database

FROM mdillon/postgis:9.5

# Dont use root to run commands in container


# https://hub.docker.com/_/postgres/
# Initialization scripts
# Add database named fminames with schemas and tables
COPY ./db-init-scripts/* /docker-entrypoint-initdb.d/

RUN useradd fminames_user
USER fminames_user
