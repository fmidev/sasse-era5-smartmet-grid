# PostgreSQL container for Fminames database without replication from FMI master database

FROM mdillon/postgis:9.5

# Dont use root to run commands in container
# USER postgres


# https://hub.docker.com/_/postgres/
# Initialization scripts
# Add database named fminames with schemas and tables
COPY ./db-init-scripts/fminames.sql /docker-entrypoint-initdb.d/fminames.sql