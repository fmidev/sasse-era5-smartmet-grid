
# Build and run postgres-database

Setup database for geonames-engine because of who knows why

`docker-compose up --detatch --build fminames-db`

# Build and run Redis

Setup database for storing grib-file details

`docker-compose up --detatch --build redis_db`

# Build and run smartmet-server

`docker-compose up --build smartmet-server`

# Fire up all three services at once

`docker-compose up --detatch`

# Read data to redis

In smartmet-server container
`docker exec smartmet-server /bin/fmi/filesys2smartmet /etc/smartmet/libraries/tools-grid/filesys-to-smartmet.cfg 0`

# Using timeseries 
`http://localhost/timeseries?param=place,utctime,WindSpeedMS:ERA5:26:0:0:0&latlon=60.192059,24.945831&format=debug&source=grid&producer=ERA5&starttime=data`