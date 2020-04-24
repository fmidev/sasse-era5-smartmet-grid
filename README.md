
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

Run a `filesys-to-smartmet`-script in the smartmet-server container... once Redis is ready. The location of filesys-to-smartmet.cfg depends on where the settings-files are located at. With `docker-compose.yaml` the settings are currently stored in `/home/smartmet/config`.

`docker exec --user smartmet smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0`

# Using timeseries

Exaple:

`/timeseries?param=place,utctime,WindSpeedMS:ERA5:26:0:0:0&latlon=60.192059,24.945831&format=debug&source=grid&producer=ERA5&starttime=data&timesteps=5`
`/timeseries?producer=ERA5&param=WindSpeedMS&latlon=60.192059,24.94583&format=debug&source=grid&&starttime=2017-08-01T00:00:00Z`
`/wfs?request=getFeature&storedquery_id=windgustcoverage&starttime=2017-08-01T00:00:00Z&endtime=2017-08-01T00:00:00Z&source=grid&bbox=21,60,24,64&crs=EPSG:4326&limits=15,999,20,999,25,999,30–999`
`/wfs?request=getFeature&storedquery_id=pressurecoverage&starttime=2017-08-01T00:00:00Z&endtime=2017-08-01T00:00:00Z&source=grid&bbox=21,60,24,64&crs=EPSG:4326&limits=0,1000`

Read data to Redis, wait for a while, and then curl the WFS like a boss:

`/bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0 && sleep 60 && curl 'localhost//wfs?request=getFeature&storedquery_id=windgustcoverage&starttime=2017-08-01T00:00:00Z&endtime=2017-08-01T00:00:00Z&source=grid&bbox=21,60,24,64&crs=EPSG:4326&limits=10,25'`

# Update process for the AMI
 1. log in to a running EC2 instace
 1. `cd ~/sasse-era5-smartmet-grid`
 1. `git pull`
 1. `docker-compose build --no-cache`
 1. Create a new AMI from the instance (with a new name)
 1. Update LaunchTemplate with id `lt-0103908425591b1a5`
  1. change version number
  1. Change AMI
 1. Change version number also to cloudformation-xx.template

# Misc notes

## Adding forest data

1. Run `aws cloudformation deploy --stack-name sasse-data-extact-debug-3 --template-file timeseries_cloudformation_forest.template`
1. Log into the created server
1. Modify _docker-compose.yml_ by adding line `- ../data/puusto:/srv/puusto/:Z` to as volume of _smartmet-server_
1. Restart smartmet server destroying the container in between (there might be a better way to do this)
1. Change directories in file _~/sasse-era5-smartmet-grid/smartmet-server/config/libraries/tools-grid/filesys-to-smartmet.cfg_ to:
   ```directories =
    [
      "/srv/data",
      "/srv/puusto",
    ]```

1. Add lines

```
1;90001;name;797;490;15.608156;59.345522;0.021995;0.021994;+x+y;Luke forest data;
```
to _/home/centos/sasse-era5-smartmet-grid/smartmet-server/config/libraries/grid-files/fmi_geometries.csv_
1. Add line `puusto;FOREST;Forest;Forest data from Luke` to _~/sasse-era5-smartmet-grid/smartmet-server/config/libraries/tools-grid/producerDef.cfg`_
1. Add line `FOREST` to _~/sasse-era5-smartmet-grid/smartmet-server/config/libraries/tools-grid/producers.cfg`_
1. Add lines
```
90001;1;FORESTAGE;Forest age from Luke;1;1;1;;
90002;1;FORESTLOCATION;;Forest location from Luke;1;1;1;;;
90003;1;FORESTDIAMETER;;Forest diameter from Luke;1;1;1;;;
90004;1;FORESTLENGTH;;Forest length from Luke;1;1;1;;;
90005;1;FORESTCANOPY;;Forest canopy cover from Luke;1;1;1;;;
90006;1;FORESTTYPE;;Forest type from Luke;1;1;1;;;
```
to _~/sasse-era5-smartmet-grid/smartmet-server/config/libraries/grid-files/fmi_parameters.csv_
1. Add lines
```
90001;171029;;
90002;29;;
90003;129030;;
90004;171030;;
90005;129029;;
90006;30;;
```
to _~/sasse-era5-smartmet-grid/smartmet-server/config/libraries/grid-files/fmi_parameterId_grib.csv_
1. Add lines
```
FOREST;90001;
```
to ~/sasse-era5-smartmet-grid/smartmet-server/config/engines/grid-engine/producers.cnf
1. Run command `docker exec --user smartmet smartmet-server /bin/fmi/filesys2smartmet /home/smartmet/config/libraries/tools-grid/filesys-to-smartmet.cfg 0`

Example query: http://ec2-34-242-23-86.eu-west-1.compute.amazonaws.com/timeseries?format=debug&starttime=data&endtime=data&source=grid&tz=utc&wkt=POLYGON((24.76268533856113 66.36894547285,28.80565408856113 64.61980368075739,31.09081033856113 62.6697800004489,27.57518533856113 62.34519816959522,21.77440408856113 62.34519816959522,24.76268533856113 66.36894547285))&param=@AVG{FORESTAGE:Forest:90001::0:0},@AVG{FORESTCANOPY:Forest:90001::0:0},@AVG{FORESTDIAMETER:Forest:90001::0:0},@AVG{FORESTLENGTH:Forest:90001::0:0},@AVG{FORESTLOCATION:Forest:90001::0:0},@AVG{FORESTTYPE:Forest:90001::0:0},@QUANTILE{.95;FORESTAGE:Forest:90001::0:0}
