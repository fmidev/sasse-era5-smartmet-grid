
# How in the…

In short:

* Start EC2 instance
* Create folder for era5-data
* Copy some data there
* Set ownership to era5-data-directory
* Clone codes from GitHub
* Build images
* Start services
* Read data to Redis
* Do things with smartmet-server

In the User Data in the Advanced settings for EC2:

```bash
#!/bin/bash

# Get docker-images and database dumps from S3
# Not necessarely required 
# aws s3 sync s3://fmi-sasse-era5/ /tmp/

# Directory for storing grib-data
sudo mkdir -p /srv/era5-data

# Copy file from S3
# Do this with CloudFormation or something ¯\_(ツ)_/¯
aws s3 cp s3://fmi-era5-world-nwp-parameters/2017/era5-201708.grib /srv/era5-data/ERA5_20170801000000_era5-201708.grib
aws s3 cp s3://fmi-era5-world-nwp-parameters/2017/era5-preprocessed-201708.grib2 /srv/era5-data/ERA5_20170801000000_era5-preprocessed-201708.grib

# Set ownership to centos user
sudo chown -R centos:centos /srv/era5-data

# User centos has the required ssh-keys
su - centos
git clone git@github.com:fmidev/sasse-era5-smartmet-grid.git
cd sasse-era5-smartmet-grid
docker-compose up -d
# end su, I don't know if this is really necessary or not.
exit
```

# Build and run postgres-database

Setup database for geonames-engine because of who knows why

`docker-compose up --detatch --build fminames-db`

# Build and run Redis

Setup database for storing grib-file details

`docker-compose up --detatch --build redis_db`

# Build and run smartmet-server

`docker-compose up --build smartmet-server`

# Fire up all three services at once

This will:

* Start the Postgresql-database and create a db-directory to store all the data there.
* Start Redis for storing information about available grib data
* Start SmartMet Server after the Postgersql is ready

`docker-compose up --detatch`

# Read data to Redis

Run a `filesys-to-smartmet`-script in the smartmet-server container... once Redis is ready.

`docker exec smartmet-server /bin/fmi/filesys2smartmet /etc/smartmet/libraries/tools-grid/filesys-to-smartmet.cfg 0`

# Using timeseries 

Exaple:

`/timeseries?param=place,utctime,WindSpeedMS:ERA5:26:0:0:0&latlon=60.192059,24.945831&format=debug&source=grid&producer=ERA5&starttime=data`