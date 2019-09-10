
# What in the…

All this is for creating contours out of ERA5 data and
storing results in a database.

When using `cloudformation.template`, you need a ready AMI that already has
the following properties.

To In short:

* Start an EC2 instance in Amazon AWS
* Log in with ssh
* Create folder for era5-data
* Set ownership to era5-data-directory
* Clone codes from GitHub
* Build Docker images
* Start containers with docker-compose
* Copy ERA5-data from S3
* Read data to Redis
* Do things with smartmet-server

In the User Data in the Advanced settings for EC2:

```bash
#!/bin/bash

# Directory for storing grib-data
sudo mkdir -p /srv/era5-data
sudo chown -R centos:centos /srv/era5-data
```

As centos user after the instance is up

```bash
cd ~/
# User centos has the required ssh-keys
git clone git@github.com:fmidev/sasse-era5-smartmet-grid.git ~/sasse

# Get docker-images and database dumps from S3
# Not necessarely required, if building from github
# aws s3 sync s3://fmi-sasse-era5/ /tmp/

# Start all services (even with --detatch the build process will wait until finished)
docker-compose up --detatch

# Copy file from S3
# Do this with CloudFormation or something ¯\_(ツ)_/¯
aws s3 cp s3://fmi-era5-world-nwp-parameters/2017/era5-201708.grib /srv/era5-data/ERA5_20170801000000_era5-201708.grib
aws s3 cp s3://fmi-era5-world-nwp-parameters/2017/era5-preprocessed-201708.grib2 /srv/era5-data/ERA5_20170801000000_era5-preprocessed-201708.grib
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

Run a `filesys-to-smartmet`-script in the smartmet-server container... once Redis is ready. The location of filesys-to-smartmet.cfg depends on where the settings-files are located at. On docker-compose.yaml the are currently set in `/home/smartmet/config`.

`docker exec --user smartmet smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0`

# Using timeseries

Exaple:

`/timeseries?param=place,utctime,WindSpeedMS:ERA5:26:0:0:0&latlon=60.192059,24.945831&format=debug&source=grid&producer=ERA5&starttime=data&timesteps=5`
`/timeseries?producer=ERA5&param=WindSpeedMS&latlon=60.192059,24.94583&format=debug&source=grid&&starttime=2017-08-01T00:00:00Z`
`/wfs?request=getFeature&storedquery_id=windgustcoverage&starttime=2017-08-01T00:00:00Z&endtime=2017-08-01T00:00:00Z&source=grid&bbox=21,60,24,64&crs=EPSG:4326&limits=10,25`
`/wfs?request=getFeature&storedquery_id=pressurecoversge&starttime=2017-08-01T00:00:00Z&endtime=2017-08-01T00:00:00Z&source=grid&bbox=21,60,24,64&crs=EPSG:4326&limits=0,1000`

Read data to Redis, wait for a while, and then curl the WFS like a boss:

`/bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0 && sleep 60 && curl 'localhost/wfs?request=getFeature&storedquery_id=Storm&starttime=2017-08-01T00:00:00Z&endtime=2017-08-01T00:00:00Z&source=grid&bbox=21,60,24,64&crs=EPSG:4326'`
