FROM centos:7.6.1810

LABEL maintainer "Teemu Sirviö <teemu.sirvio@fmi.fi>"

RUN yum clean all

RUN rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm 
RUN rpm -ivh https://download.postgresql.org/pub/repos/yum/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-3.noarch.rpm 
RUN rpm -ivh https://download.fmi.fi/smartmet-open/rhel/7/x86_64/smartmet-open-release-17.9.28-1.el7.fmi.noarch.rpm

RUN yum-config-manager --disable "pgdg*" 
RUN yum-config-manager --enable "pgdg95"

# Install 9.5 version before postgis to prevent 9.2 from being installed
RUN yum -y install postgresql95

# This should install from epel
RUN yum -y install postgis

# RUN yum -y update
RUN yum -y install unzip 
RUN yum -y install smartmet-plugin-backend 
RUN yum -y install smartmet-plugin-admin 
RUN yum -y install smartmet-plugin-gribtimeseries 
RUN yum -y install smartmet-plugin-grid-admin 
RUN yum -y install smartmet-plugin-grid-gui 
RUN yum -y install smartmet-plugin-gribwfs 
RUN yum -y install smartmet-tools-grid 
RUN yum clean all 

# For installing filesys2smartmet which is used to load grib-files to redis

HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost/admin?what=qengine || exit 1

# wms.conf defines imagecache. timeseriescache's use is yet to be found.
RUN mkdir -p /var/log/smartmet /var/smartmet/timeseriescache /var/smartmet/imagecache

RUN mkdir -p /srv/data
RUN useradd smartmet
RUN chown -R smartmet /srv/data /var/log/smartmet /var/smartmet/timeseriescache /var/smartmet/imagecache

# Dont use root to run commands in container
USER smartmet

# Smartmet Servers configs should be separate from /etc's settings that come from RPM-packages
# These locations are required to be defined in several different setting files under the config-direcotry

COPY --chown=smartmet scripts /home/smartmet/scripts 

# Uncomment to include files in Docker image. 
# Comment and add in compose-file for development
#COPY --chown=smartmet config /home/smartmet/config 


# ENTRYPOINT ["/docker-entrypoint.sh"]
# CMD ["smartmetd"]