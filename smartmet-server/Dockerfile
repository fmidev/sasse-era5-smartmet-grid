FROM centos:7.6.1810

LABEL maintainer "Teemu Sirviö <teemu.sirvio@fmi.fi>"

RUN yum clean all

# Add epel repository for intalling postgis and other packages
RUN rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm 

# Add pgdg repository for installing postgresql (but only a certain version)
RUN rpm -ivh https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-3.noarch.rpm 

# Add smartmet-open repository for installing FMI's opensource packages 
RUN rpm -ivh https://download.fmi.fi/smartmet-open/rhel/7/x86_64/smartmet-open-release-17.9.28-1.el7.fmi.noarch.rpm

# Make only 9.5 version postgres repository available
RUN yum-config-manager --disable "pgdg*" 
RUN yum-config-manager --enable "pgdg95"

# Install version 9.5  before postgis to prevent 9.2 from being installed
# The version 9.5 seems to be a dependency for smartmet-tools-grid
RUN yum -y install postgresql95

# This should install from epel
# Postgis requires some libraries that are installed with postgresql
# The postgres95 should be installed before postgis to prevent wrong versions
# being installed as a dependency
RUN yum -y install postgis

# The order of packages installed seems to affect dependencies from working 
RUN yum -y install smartmet-plugin-backend 
RUN yum -y install smartmet-plugin-admin 
RUN yum -y install smartmet-plugin-gribtimeseries 
RUN yum -y install smartmet-plugin-grid-admin 
RUN yum -y install smartmet-plugin-grid-gui 
RUN yum -y install smartmet-plugin-gribwfs 
# For installing filesys2smartmet which is used to load grib-files to redis
RUN yum -y install smartmet-tools-grid 
RUN yum clean all 


HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost/admin?what=qengine || exit 1

# wms.conf defines imagecache. timeseriescache's use is yet to be found.
RUN mkdir -p /var/log/smartmet /var/smartmet/timeseriescache /var/smartmet/imagecache

RUN mkdir -p /srv/data
RUN useradd smartmet
RUN chown -R smartmet /srv/data /var/log/smartmet /var/smartmet/timeseriescache /var/smartmet/imagecache

# Smartmet Servers configs should be separate from /etc's settings that come from RPM-packages
# These locations are required to be defined in several different setting files under the config-direcotry
COPY scripts /home/smartmet/scripts 
RUN chown -R smartmet /home/smartmet/scripts

# Dont use root to run commands in container
USER smartmet

# Uncomment to include files in Docker image. 
# Comment and add in compose-file for development
#COPY --chown=smartmet config /home/smartmet/config 

# ENTRYPOINT ["/docker-entrypoint.sh"]
# CMD ["smartmetd"]



