
# Setup database for geonames-engine because raisins

`docker-compose up --detatch --build fminames-db`

# Setup database for storing grib-file details

`docker-compose up --detatch --build redis_db`

# Setup SmartMet Server

## Build and run

`docker-compose up --build smartmet-server`

## Read data to redis

Log in to smartmet-server container
`docker exec -ti smartmet-server bash`

Then
`/bin/fmi/filesys2smartmet /etc/smartmet/libraries/tools-grid/filesys-to-smartmet.cfg 0`

`/timeseries?param=place,utctime,WindSpeedMS:ERA5:26:0:0:0&latlon=60.192059,24.945831&format=debug&source=grid&producers=ERA5&starttime=2017-08-01T00:00:00Z`